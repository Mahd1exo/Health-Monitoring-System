package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

// Define structures for OpenAI and response handling
type OpenAIRequest struct {
	Model    string        `json:"model"`
	Messages []ChatMessage `json:"messages"`
}

type ChatMessage struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

type OpenAIResponse struct {
	Choices []struct {
		Message struct {
			Content string `json:"content"`
		} `json:"message"`
	} `json:"choices"`
}

type HealthRequest struct {
	Temp     float64 `json:"temp"`
	Pulse    float64 `json:"pulse"`
	SpO2     float64 `json:"spO2"`
	Language string  `json:"language"`
}

type HealthResponse struct {
	Suggestion string `json:"suggestion"`
}

// Function to interact with OpenAI API
func GetHealthSuggestion(temp, pulse, spO2 float64, language string) (string, error) {
	url := "https://api.openai.com/v1/chat/completions"
	apiKey := "" // Replace with your OpenAI API key

	// Setup chat messages
	messages := []ChatMessage{
		{Role: "system", Content: "You are a health monitoring assistant."},
		{Role: "user", Content: fmt.Sprintf(`
            A patient has the following health readings:
            - Body Temperature: %.1f°C
            - Pulse Rate: %.1f BPM
            - SpO₂ Level: %.1f%%
            
            Based on these values, please provide a health assessment and any recommendations in %s.
        `, temp, pulse, spO2, language)},
	}

	// Serialize request
	requestBody := OpenAIRequest{
		Model:    "gpt-3.5-turbo",
		Messages: messages,
	}
	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		return "", fmt.Errorf("error serializing request: %v", err)
	}

	// Set up the HTTP request
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		return "", fmt.Errorf("error creating request: %v", err)
	}
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+apiKey)

	// Send request and parse response
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return "", fmt.Errorf("error sending request: %v", err)
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("error reading response: %v", err)
	}

	var openAIResp OpenAIResponse
	if err := json.Unmarshal(body, &openAIResp); err != nil {
		return "", fmt.Errorf("error parsing response: %v", err)
	}

	if len(openAIResp.Choices) > 0 {
		return openAIResp.Choices[0].Message.Content, nil
	}
	return "", fmt.Errorf("no suggestions returned from OpenAI")
}

// Handler for the Go service
func suggestionHandler(w http.ResponseWriter, r *http.Request) {
	var req HealthRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request payload", http.StatusBadRequest)
		return
	}

	suggestion, err := GetHealthSuggestion(req.Temp, req.Pulse, req.SpO2, req.Language)
	if err != nil {
		http.Error(w, "Failed to get suggestion: "+err.Error(), http.StatusInternalServerError)
		return
	}

	response := HealthResponse{Suggestion: suggestion}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

// Start the Go server
func main() {
	http.HandleFunc("/suggest", suggestionHandler)
	fmt.Println("Starting server on port 8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
