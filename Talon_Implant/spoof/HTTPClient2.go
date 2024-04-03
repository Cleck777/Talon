package clients

import (
	"bytes"
	"crypto/tls"
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
	"time"
)
type HTTPClient struct {
	client  *http.Client
	config  ClientConfig
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


func (h *HTTPClient) StartCommunication(client *http.Client, config ClientConfig) {
	switch config.Mode {
	case "session":
		// Use the session-based approach to communicate
		fmt.Println("Starting session-based communication...")
		response, err := Read(client, config.URL)
		if err != nil {
			fmt.Println("Error in session-based communication:", err)
		} else {
			fmt.Println("Session response:", response)
		}
	case "beacon":
		// Use the beaconing approach to communicate
		fmt.Println("Starting beaconing...")
		StartBeaconing(client, config.URL, config.BeaconInterval, config.BeaconData)
	default:
		fmt.Println("Invalid mode specified in configuration.")
	}
}

// HTTPStartSession starts a new HTTP session.
func (h *HTTPClient) HTTPStartSession(address string) (*http.Client, error) {
	client := &http.Client{
		Transport: &http.Transport{
			Proxy: http.ProxyFromEnvironment,
			TLSClientConfig: &tls.Config{
				InsecureSkipVerify: true,
			},
		},
	}
	return client, nil
}

// Read sends a GET request to the specified URL and returns the response body.
func (h *HTTPClient) Read(client *http.Client, url string) (string, error) {
	resp, err := client.Get(url)
	if err != nil {
		return "", fmt.Errorf("got error when requesting URL: %s", err)
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("got error when reading response body: %s", err)
	}

	return strings.Trim(string(body), "\n\r"), nil
}

// Write sends a POST request to the specified URL with the given payload and returns the response body.
func (h *HTTPClient) Write(client *http.Client, url string, payload []byte) ([]byte, error) {
	resp, err := client.Post(url, "application/json", bytes.NewBuffer(payload))
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	return body, nil
}
func (h *HTTPClient) StartBeaconing(client *http.Client, url string, interval time.Duration, data []byte) {
	ticker := time.NewTicker(interval)
	quit := make(chan struct{})
	go func() {
		for {
			select {
			case <-ticker.C:
				if len(data) == 0 {
					// Send a GET request
					response, err := Read(client, url)
					if err != nil {
						fmt.Println("Error beaconing (GET):", err)
					} else {
						fmt.Println("Beacon sent (GET), response:", response)
					}
				} else {
					// Send a POST request
					response, err := Write(client, url, data)
					if err != nil {
						fmt.Println("Error beaconing (POST):", err)
					} else {
						fmt.Println("Beacon sent (POST), response:", string(response))
					}
				}
			case <-quit:
				ticker.Stop()
				return
			}
		}
	}()
}
/*
func main() {
	// Example configuration for beaconing
	config := ClientConfig{
		Mode:           "beacon",
		URL:            "http://example.com/beacon",
		BeaconInterval: 10 * time.Second,
	}

	// Or, to use a session-based approach
	// config := ClientConfig{
	//     Mode: "session",
	//     URL:  "http://example.com/session",
	// }

	client, err := HTTPStartSession(config.URL)
	if err != nil {
		fmt.Println("Error creating HTTP client:", err)
		return
	}

	StartCommunication(client, config)

	// Note: To stop beaconing in this example, you'd need to implement a way to send a signal to the quit channel in StartBeaconing.
}*/