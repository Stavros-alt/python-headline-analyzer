import tkinter as tk
from tkinter import scrolledtext
from textblob import TextBlob

# --- 1. THE ANALYSIS ENGINE ---

# Predefined lists of marketing words
POWER_WORDS = {
    'amazing', 'secret', 'powerful', 'proven', 'guaranteed', 'effortless', 'best', 'you',
    'free', 'new', 'discover', 'ultimate', 'simple', 'exclusive', 'instantly'
}
URGENCY_WORDS = {
    'now', 'today', 'hurry', 'limited', 'final', 'deadline', 'urgent', 'act now'
}

def analyze_headline(headline):
    """
    Performs a full NLP and marketing analysis on a given headline string.
    Returns a dictionary with the analysis results.
    """
    results = {}
    blob = TextBlob(headline)
    words = [word.lower() for word in blob.words]

    # a) Sentiment Analysis
    sentiment_score = blob.sentiment.polarity
    if sentiment_score > 0.1:
        results['Sentiment'] = f"Positive (Score: {sentiment_score:.2f})"
    elif sentiment_score < -0.1:
        results['Sentiment'] = f"Negative (Score: {sentiment_score:.2f})"
    else:
        results['Sentiment'] = f"Neutral (Score: {sentiment_score:.2f})"

    # b) Word and Character Count
    results['Word Count'] = len(words)
    results['Character Count'] = len(headline)

    # c) Keyword Analysis (extracting nouns)
    nouns = [word for word, tag in blob.tags if tag.startswith('NN')]
    results['Key Nouns'] = ', '.join(set(nouns)) if nouns else 'None'

    # d) Marketing Word Analysis
    found_power_words = POWER_WORDS.intersection(words)
    results['Power Words'] = ', '.join(found_power_words) if found_power_words else 'None'

    found_urgency_words = URGENCY_WORDS.intersection(words)
    results['Urgency Words'] = ', '.join(found_urgency_words) if found_urgency_words else 'None'
    
    return results

# --- 2. THE GUI APPLICATION ---

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Headline Analyzer")
        self.root.geometry("600x650")
        self.root.configure(bg="#2d3436")

        # --- Widget Creation ---
        main_frame = tk.Frame(root, bg="#2d3436", padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Input Label & Entry
        input_label = tk.Label(main_frame, text="Enter Your Headline Below:", font=("Arial", 14), bg="#2d3436", fg="white")
        input_label.pack(pady=(0, 10))

        self.headline_entry = tk.Entry(main_frame, font=("Arial", 14), width=50, relief=tk.FLAT, bd=5)
        self.headline_entry.pack(pady=(0, 20), ipady=10)
        
        # Analyze Button
        self.analyze_btn = tk.Button(main_frame, text="ANALYZE HEADLINE", command=self.perform_analysis, font=("Arial", 14, "bold"), bg="#0984e3", fg="white", relief=tk.FLAT, padx=20, pady=10)
        self.analyze_btn.pack()

        # Results Area
        results_label = tk.Label(main_frame, text="RESULTS:", font=("Arial", 14), bg="#2d3436", fg="white")
        results_label.pack(pady=(30, 10))

        self.results_text = scrolledtext.ScrolledText(main_frame, font=("Arial", 12), height=15, width=60, relief=tk.FLAT, bd=5, bg="#636e72", fg="white")
        self.results_text.pack()
        self.results_text.config(state=tk.DISABLED) # Make it read-only initially

    # --- Widget Functions ---
    def perform_analysis(self):
        """Gets headline, runs analysis, and displays formatted results."""
        headline = self.headline_entry.get()
        if not headline.strip():
            # If input is empty, clear the results
            self.display_results("Please enter a headline to analyze.")
            return

        analysis_results = analyze_headline(headline)
        
        # Format the results for display
        formatted_output = ""
        for key, value in analysis_results.items():
            formatted_output += f"-> {key}:\n   {value}\n\n"
        
        self.display_results(formatted_output)

    def display_results(self, text):
        """Helper function to safely update the results text area."""
        self.results_text.config(state=tk.NORMAL) # Make it writable
        self.results_text.delete('1.0', tk.END)    # Clear previous content
        self.results_text.insert(tk.END, text)     # Insert new content
        self.results_text.config(state=tk.DISABLED) # Make it read-only again

# --- 3. RUN THE APPLICATION ---
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()