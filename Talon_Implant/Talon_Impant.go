package main

/* Talon C2 - Implant
Copyright (C) 2024  Cleck777

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>

*/
import (
	"os/exec"
	"runtime"
)

const host = "localhost"
const port = "443"

// constants
var (
	// TalonID is the unique identifier for the implant
	TalonID string
	os	  string

)
func init() {
	// Get the operating system
	os := runtime.GOOS
	id,er := uuid.Newv4()
	if err != nil {
	}
	TalonID := id.String()
}
func main() {


	startBeacon()

}

func startBeacon() {
	// Get the operating system
	os := runtime.GOOS

	// Get the command to execute
	var cmd *exec.Cmd
	if os == "windows" {
		if cmd
	} else {

	}

	// Execute the command
	cmd.Run()
}
