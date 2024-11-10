use actix_web::{post, web, App, HttpResponse, HttpServer, Responder};
use reqwest::Client;
use serde::{Deserialize, Serialize};
use serde_json::json;
use std::env;

#[derive(Deserialize)]
struct HealthRequest {
    temp: f64,
    pulse: f64,
    spO2: f64,
    language: String,
}

#[derive(Serialize)]
struct HealthResponse {
    suggestion: String,
}

#[derive(Serialize)]
struct OpenAIRequest {
    model: String,
    messages: Vec<ChatMessage>,
}

#[derive(Serialize)]
struct ChatMessage {
    role: String,
    content: String,
}

#[derive(Deserialize)]
struct OpenAIResponse {
    choices: Vec<Choice>,
}

#[derive(Deserialize)]
struct Choice {
    message: Message,
}

#[derive(Deserialize)]
struct Message {
    content: String,
}

// Function to interact with the OpenAI API
async fn get_health_suggestion(temp: f64, pulse: f64, spO2: f64, language: &str) -> Result<String, reqwest::Error> {
    let url = "https://api.openai.com/v1/chat/completions";
    let api_key = "", // Add your OpenAi API key
    // Set up chat messages
    let messages = vec![
        ChatMessage {
            role: "system".to_string(),
            content: "You are a health monitoring assistant.".to_string(),
        },
        ChatMessage {
            role: "user".to_string(),
            content: format!(
                "A patient has the following health readings:\n- Body Temperature: {:.1}°C\n- Pulse Rate: {:.1} BPM\n- SpO₂ Level: {:.1}%\n\nBased on these values, please provide a health assessment and any recommendations in {}.",
                temp, pulse, spO2, language
            ),
        },
    ];

    // Prepare OpenAI request
    let request_body = OpenAIRequest {
        model: "gpt-3.5-turbo".to_string(),
        messages,
    };

    // Send request to OpenAI
    let client = Client::new();
    let response = client
        .post(url)
        .header("Authorization", format!("Bearer {}", api_key))
        .json(&request_body)
        .send()
        .await?;

    // Parse response
    let openai_response: OpenAIResponse = response.json().await?;
    if let Some(choice) = openai_response.choices.get(0) {
        Ok(choice.message.content.clone())
    } else {
        Ok("No suggestion available.".to_string())
    }
}

// Handler for the health suggestion service
#[post("/suggest")]
async fn suggestion_handler(req: web::Json<HealthRequest>) -> impl Responder {
    match get_health_suggestion(req.temp, req.pulse, req.spO2, &req.language).await {
        Ok(suggestion) => HttpResponse::Ok().json(HealthResponse { suggestion }),
        Err(err) => HttpResponse::InternalServerError().body(format!("Failed to get suggestion: {}", err)),
    }
}

// Start the Actix Web server
#[actix_web::main]
async fn main() -> std::io::Result<()> {
    println!("Starting server on http://127.0.0.1:8080");
    HttpServer::new(|| {
        App::new()
            .service(suggestion_handler)
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}
