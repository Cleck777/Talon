package HTTPClient

import (
	"bytes"
	"crypto/tls"
	"io/ioutil"
	"net/http"
)

// HTTPStartSession starts a new HTTP session.
func HTTPStartSession(address string) (*http.Client, error) {
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
func Read(client *http.Client, url string) ([]byte, error) {
	resp, err := client.Get(url)
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

// Write sends a POST request to the specified URL with the given payload and returns the response body.
func Write(client *http.Client, url string, payload []byte) ([]byte, error) {
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
