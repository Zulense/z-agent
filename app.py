import gradio as gr

# 1. Define your dictionary of videos and their contexts
# You can easily expand this to 10 or more items.
VIDEO_DATABASE = {
    "Multi-Head Attention": {
        "url": "./papers-context/transformer-paper/MultiHeadAttentionScene_3.mp4",
        "context": "Topic: Multi-Head Attention: Diverse Perspectives for Enhanced Context"
    },
    "Scaled Dot-Product Attention": {
        "url": "./papers-context/transformer-paper/Scaled_Dot-Product_Attention_The_Mathematical_Core_2.mp4",
        "context": "Topic: Scaled Dot-Product Attention: The Core of Contextual Understanding"
    },
    "Residual Connections": {
        "url": "./papers-context/deepseek_mhc_renders/deepseek_mhc_animation_0.mp4",
        "context": "Topic: Residual Connections: The Foundation for Deep Networks, and Hyper-Connections (HC)"
    },
    "Unveiling the Pitfalls": {
        "url": "./papers-context/deepseek_mhc_renders/deepseek_mhc_animation_1.mp4",
        "context": "Topic: Unveiling the Pitfalls: Hyper-Connections' Instability and Memory Demands"
    },
    "mHC": {
        "url": "./papers-context/deepseek_mhc_renders/deepseek_mhc_animation_2.mp4",
        "context": "mHC: The Manifold Approach to Stable Hyper-Connections"
    },
    "Projecting to Stability": {
        "url": "./papers-context/deepseek_mhc_renders/deepseek_mhc_animation_3.mp4",
        "context": "Topic: Projecting to Stability: Parameterizing mHC with Sinkhorn-Knopp"
    },
}

# Extract the titles to use in our dropdown menu
video_titles = list(VIDEO_DATABASE.keys())

def load_video_data(selected_title):
    """
    Triggered when the user changes the dropdown selection.
    Fetches the corresponding URL and context from the dictionary.
    """
    if not selected_title:
        return None, ""
    
    # Get the dictionary entry for the selected video
    data = VIDEO_DATABASE[selected_title]
    return data["url"], data["context"]

def process_displayed_data(video_path, context):
    """
    Simulates your backend analysis on whatever is currently on the screen.
    """
    if not video_path:
        return "⚠️ Please select a video from the dropdown first."
    
    return (
        f"✅ Successfully processed the current video!\n\n"
        f"🔗 URL: {video_path}\n"
        f"📝 Context snippet: {context[:40]}..."
    )

# Build the User Interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎥 Video Database Viewer")
    gr.Markdown("Select a video from the dropdown to load its content and context.")
    
    # The Dropdown selector
    # We set 'value' to the first item so the dashboard isn't empty on load
    video_selector = gr.Dropdown(
        choices=video_titles, 
        value=video_titles[0], 
        label="Select a Video to Load",
        interactive=True
    )
    
    gr.Markdown("---")
    
    with gr.Row():
        # Left Column: The Video Player (Locked)
        with gr.Column():
            video_display = gr.Video(
                label="Current Video",
                interactive=False
            )
            
        # Right Column: The Context and Actions (Locked)
        with gr.Column():
            context_display = gr.Textbox(
                label="Associated Context", 
                lines=6,
                interactive=False
            )
            
            

    # --- WIRING IT TOGETHER ---
    
    # 1. When the dropdown changes, update the video player and context box
    video_selector.change(
        fn=load_video_data,
        inputs=[video_selector],
        outputs=[video_display, context_display]
    )
    
    # 2. When the app first loads, trigger the dropdown change to populate the first video
    demo.load(
        fn=load_video_data,
        inputs=[video_selector],
        outputs=[video_display, context_display]
    )

   

if __name__ == "__main__":
    demo.launch(debug=True)