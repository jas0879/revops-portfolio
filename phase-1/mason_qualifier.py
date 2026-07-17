import dash
from dash import dcc, html, Input, Output, State
import requests
import json

app = dash.Dash(__name__)

CF_KNOWLEDGE = """
You are Mason, a friendly and professional AI qualification assistant for Contractor Foreman (CF).
Contractor Foreman is a construction management software platform built specifically for contractors.

ABOUT CONTRACTOR FOREMAN:
- Purpose: Project management software built specifically for contractors
- Best for: General contractors, specialty trades (electrical, plumbing, HVAC, roofing, etc.), home builders, remodelers
- Key features: Project management, scheduling, estimates, invoicing, subcontractor management, daily logs, time tracking, document storage, client portal
- Pricing: Basic $49/mo, Standard $105/mo, Plus $166/mo, Pro $221/mo, Unlimited $332/mo (annual billing)
- Free 30-day trial available
- 100-day money back guarantee
- Integrates with QuickBooks
- Used by thousands of contractors across the US

QUALIFICATION CRITERIA - A lead is QUALIFIED if:
- They are a contractor or work in construction-related business
- They have a real business (not a student or researcher)
- They are actively looking for software (not just browsing)
- They are not a competitor or developer testing the system

DISQUALIFICATION CRITERIA - Do NOT book demo if:
- They are NOT in construction (hair salons, accounting firms, restaurants, etc.)
- They are a student, researcher, or competitor
- They have no budget and are just exploring with no real intent

YOUR CONVERSATION FLOW:
1. Warm greeting - introduce yourself as Mason from Contractor Foreman
2. Ask what type of contracting work they do (QUALIFICATION CHECK - must be construction related)
3. Ask about their team size
4. Ask about their biggest challenge managing projects
5. Ask if they are currently using any software
6. Ask about their timeline to get started
7. Based on answers - either:
   QUALIFIED: "Great news! Based on what you've shared, Contractor Foreman sounds like a great fit. I'd love to set you up with one of our specialists for a personalized demo. Can I get your name and email?"
   NOT QUALIFIED: "Thank you for your time! Based on what you've shared, our full demo might not be the best use of your time right now. I'd recommend starting with our free 30-day trial at contractorforeman.com - no credit card needed!"

PERSONALITY:
- Friendly, professional, and conversational
- Sound like a knowledgeable team member, not a robot
- Keep responses concise - 2-3 sentences max per message
- Ask ONE question at a time
- If they ask about pricing, features, or integrations - answer briefly then continue qualifying
- Never be pushy or aggressive
- Always be respectful even when disqualifying

IMPORTANT: Start by greeting them warmly and asking your first qualifying question. Keep it natural.
"""

DARK = "#0f1117"
CARD = "#1e2130"
TEAL = "#1A6B72"
WHITE = "white"
GRAY = "#888"
LIGHT_GRAY = "#ccc"

app.layout = html.Div(style={
    "backgroundColor": DARK,
    "minHeight": "100vh",
    "fontFamily": "Arial",
    "display": "flex",
    "flexDirection": "column",
    "alignItems": "center",
    "justifyContent": "center",
    "padding": "20px"
}, children=[

    # Header
    html.Div(style={"textAlign": "center", "marginBottom": "24px"}, children=[
        html.Div(style={
            "width": "64px", "height": "64px", "borderRadius": "50%",
            "backgroundColor": TEAL, "display": "flex", "alignItems": "center",
            "justifyContent": "center", "margin": "0 auto 12px auto",
            "fontSize": "28px"
        }, children="🏗️"),
        html.H1("Mason", style={"color": WHITE, "margin": "0", "fontSize": "28px"}),
        html.P("AI Qualification Assistant | Contractor Foreman",
               style={"color": GRAY, "margin": "4px 0 0 0", "fontSize": "14px"}),
        html.Div(style={
            "display": "inline-flex", "alignItems": "center", "gap": "6px",
            "backgroundColor": "#1a3a1a", "padding": "4px 12px", "borderRadius": "20px",
            "marginTop": "8px"
        }, children=[
            html.Div(style={"width": "8px", "height": "8px", "borderRadius": "50%", "backgroundColor": "#4CAF50"}),
            html.Span("Online", style={"color": "#4CAF50", "fontSize": "12px"})
        ])
    ]),

    # Chat Container
    html.Div(style={
        "backgroundColor": CARD,
        "borderRadius": "16px",
        "width": "100%",
        "maxWidth": "680px",
        "height": "520px",
        "display": "flex",
        "flexDirection": "column",
        "overflow": "hidden",
        "boxShadow": "0 8px 32px rgba(0,0,0,0.4)"
    }, children=[

        # Messages Area
        html.Div(id="messages-area", style={
            "flex": "1",
            "overflowY": "auto",
            "padding": "20px",
            "display": "flex",
            "flexDirection": "column",
            "gap": "16px"
        }),

        # Input Area
        html.Div(style={
            "padding": "16px",
            "borderTop": f"1px solid #2a2f3f",
            "display": "flex",
            "gap": "12px",
            "alignItems": "center"
        }, children=[
            dcc.Input(
                id="user-input",
                type="text",
                placeholder="Type your message...",
                style={
                    "flex": "1",
                    "backgroundColor": "#0f1117",
                    "border": f"1px solid #2a2f3f",
                    "borderRadius": "24px",
                    "padding": "12px 18px",
                    "color": WHITE,
                    "fontSize": "14px",
                    "outline": "none"
                },
                n_submit=0,
                debounce=False
            ),
            html.Button(
                "Send",
                id="send-button",
                n_clicks=0,
                style={
                    "backgroundColor": TEAL,
                    "color": WHITE,
                    "border": "none",
                    "borderRadius": "24px",
                    "padding": "12px 24px",
                    "cursor": "pointer",
                    "fontSize": "14px",
                    "fontWeight": "bold",
                    "whiteSpace": "nowrap"
                }
            )
        ])
    ]),

    # Footer
    html.P(
        "Powered by Contractor Foreman | Built by Jose Arzaga",
        style={"color": "#444", "fontSize": "11px", "marginTop": "16px"}
    ),

    # Store conversation history
    dcc.Store(id="conversation-store", data=[]),
    dcc.Store(id="initialized-store", data=False),
])


def mason_bubble(text):
    return html.Div(style={"display": "flex", "gap": "10px", "alignItems": "flex-start"}, children=[
        html.Div(style={
            "width": "36px", "height": "36px", "borderRadius": "50%",
            "backgroundColor": TEAL, "display": "flex", "alignItems": "center",
            "justifyContent": "center", "flexShrink": "0", "fontSize": "16px"
        }, children="🏗️"),
        html.Div(style={
            "backgroundColor": "#2a2f3f",
            "borderRadius": "0 16px 16px 16px",
            "padding": "12px 16px",
            "maxWidth": "85%",
            "color": WHITE,
            "fontSize": "14px",
            "lineHeight": "1.5"
        }, children=text)
    ])


def user_bubble(text):
    return html.Div(style={"display": "flex", "justifyContent": "flex-end"}, children=[
        html.Div(style={
            "backgroundColor": TEAL,
            "borderRadius": "16px 0 16px 16px",
            "padding": "12px 16px",
            "maxWidth": "85%",
            "color": WHITE,
            "fontSize": "14px",
            "lineHeight": "1.5"
        }, children=text)
    ])


def call_mason(conversation_history):
    messages = [{"role": "system", "content": CF_KNOWLEDGE}]
    for msg in conversation_history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "llama3.1",
                "messages": messages,
                "stream": False,
                "options": {"temperature": 0.7, "num_predict": 200}
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json()["message"]["content"]
        else:
            return "I'm having trouble connecting right now. Please try again in a moment."
    except Exception as e:
        return "I'm having trouble connecting right now. Please try again in a moment."


@app.callback(
    Output("messages-area", "children"),
    Output("conversation-store", "data"),
    Output("user-input", "value"),
    Output("initialized-store", "data"),
    Input("send-button", "n_clicks"),
    Input("user-input", "n_submit"),
    State("user-input", "value"),
    State("conversation-store", "data"),
    State("initialized-store", "data"),
    State("messages-area", "children"),
    prevent_initial_call=False
)
def handle_conversation(n_clicks, n_submit, user_text, conversation, initialized, current_messages):
    messages_display = current_messages or []
    
    # Initialize Mason's greeting
    if not initialized:
        greeting = call_mason([])
        conversation = [{"role": "assistant", "content": greeting}]
        messages_display = [mason_bubble(greeting)]
        return messages_display, conversation, "", True

    # Handle user input
    if not user_text or not user_text.strip():
        return messages_display, conversation, "", initialized

    # Add user message
    user_msg = user_text.strip()
    conversation.append({"role": "user", "content": user_msg})
    messages_display.append(user_bubble(user_msg))

    # Get Mason's response
    mason_response = call_mason(conversation)
    conversation.append({"role": "assistant", "content": mason_response})
    messages_display.append(mason_bubble(mason_response))

    return messages_display, conversation, "", initialized


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8051, debug=False)
