package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"regexp"
	"strings"

	"github.com/google/generative-ai-go/genai"
	"google.golang.org/api/option"
	"github.com/joho/godotenv"
)

// Define the structure for health request and response
type HealthRequest struct {
	Temp     float64 `json:"temp"`
	Pulse    float64 `json:"pulse"`
	SpO2     float64 `json:"spO2"`
	Language string  `json:"language"`
}

type HealthResponse struct {
	Suggestion string `json:"suggestion"`
}

// Function to interact with Gemini API
func GetHealthSuggestion(temp, pulse, spO2 float64, language string) (string, error) {
	// Load API key from .env file
	err := godotenv.Load()
	if err != nil {
		return "", fmt.Errorf("error loading .env file")
	}
	apiKey := os.Getenv("GEMINI_API_KEY")
	if apiKey == "" {
		return "", fmt.Errorf("API key not set in environment")
	}

	// Create a new context and Gemini client
	ctx := context.Background()
	client, err := genai.NewClient(ctx, option.WithAPIKey(apiKey))
	if err != nil {
		return "", fmt.Errorf("failed to create Gemini client: %v", err)
	}

	// Choose model and prepare the prompt for health suggestions
	model := client.GenerativeModel("gemini-1.5-flash")
	prompt := fmt.Sprintf(
		`A patient has the following health readings:
		- Body Temperature: %.1f°C
		- Pulse Rate: %.1f BPM
		- SpO₂ Level: %.1f%%
		Based on these values, please provide a health assessment and any recommendations in %s.`,
		temp, pulse, spO2, language,
	)

	// Generate content using Gemini
	resp, err := model.GenerateContent(ctx, genai.Text(prompt))
	if err != nil {
		return "", fmt.Errorf("failed to generate content: %v", err)
	}

	// Attempt to extract the suggestion from the response
	if len(resp.Candidates) > 0 && resp.Candidates[0].Content != nil {
		rawContent := fmt.Sprintf("%+v", resp.Candidates[0].Content)
		cleanedContent := postProcessContent(rawContent)
		return cleanedContent, nil
	}

	return "", fmt.Errorf("no suggestions returned from Gemini")
}

// Helper function to clean up the response content
func postProcessContent(rawContent string) string {
	// Remove specific prefixes and suffixes
	rawContent = strings.ReplaceAll(rawContent, "Parts:", "")
	rawContent = strings.ReplaceAll(rawContent, "Role:model", "")

	// Regular expression to remove symbols like &, { }, Markdown headings and extra asterisks
	re := regexp.MustCompile(`[&{}#\[\]\*]+`)
	cleaned := re.ReplaceAllString(rawContent, "")

	// Replace double newlines with single newline for clean formatting
	cleaned = strings.ReplaceAll(cleaned, "\n\n", "\n")

	// Trim any extra whitespace at the start and end
	cleaned = strings.TrimSpace(cleaned)

	return cleaned
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
