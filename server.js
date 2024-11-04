// Import required modules
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const puppeteer = require('puppeteer');
const axios = require('axios');
require('dotenv').config(); // Load environment variables from .env file

const app = express();
const PORT = process.env.PORT || 5000;  // Use the PORT from environment variables if available

app.use(cors());
app.use(bodyParser.json());

// Root URL route for testing server functionality
app.get('/', (req, res) => {
    res.send('Hello World! The server is working.');
});

// Endpoint to generate notes using Hugging Face Inference API
app.post('/generate-notes', async (req, res) => {
    const userInput = req.body.text;

    // Validate input
    if (!userInput || typeof userInput !== 'string') {
        return res.status(400).json({ error: 'Invalid input, expected a string.' });
    }

    try {
        // Call Hugging Face's Inference API with the GPT-2 model (or another model)
        const response = await axios.post(
            'https://api-inference.huggingface.co/models/gpt2',  // Change model if needed
            { inputs: userInput },
            {
                headers: {
                    Authorization: `Bearer ${process.env.HUGGING_FACE_API_KEY}`,  // Use your Hugging Face API key
                },
            }
        );

        // Check if the response is valid
        if (response.data && response.data.length > 0 && response.data[0].generated_text) {
            const notes = response.data[0].generated_text.trim(); // Extract the generated text
            res.json({ notes });
        } else {
            res.status(500).json({ error: 'Failed to generate notes. No response from Hugging Face.' });
        }
    } catch (error) {
        // Log and return the error
        console.error('Error with Hugging Face API:', error.response ? error.response.data : error.message);
        res.status(500).json({ error: 'Failed to generate notes', details: error.response ? error.response.data : error.message });
    }
});

// Function to scrape Google search results using Puppeteer
async function scrapeGoogle(query) {
    let browser;
    try {
        // Launch Puppeteer in headless mode
        browser = await puppeteer.launch({ headless: true });
        const page = await browser.newPage();
        await page.goto(`https://www.google.com/search?q=${encodeURIComponent(query)}`);
        await page.waitForSelector('.tF2Cxc');

        // Extract search results
        const results = await page.evaluate(() => {
            const data = [];
            const items = document.querySelectorAll('.tF2Cxc');
            items.forEach((item) => {
                const title = item.querySelector('.DKV0Md').innerText;
                const link = item.querySelector('.yuRUbf a').href;
                const snippet = item.querySelector('.IsZvec').innerText;
                data.push({ title, link, snippet });
            });
            return data;
        });

        return results;
    } finally {
        if (browser) {
            await browser.close();  // Always close the browser
        }
    }
}

// Endpoint for searching Google
app.post('/search-google', async (req, res) => {
    const searchQuery = req.body.query;

    // Validate input
    if (!searchQuery || typeof searchQuery !== 'string') {
        return res.status(400).json({ error: 'Invalid input, expected a string.' });
    }

    try {
        const results = await scrapeGoogle(searchQuery);
        res.json({ results });
    } catch (error) {
        console.error('Error scraping Google:', error);
        res.status(500).json({ error: 'Failed to scrape Google search results', details: error.message });
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

