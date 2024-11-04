document.getElementById('generate').addEventListener('click', async () => {
    const inputText = document.getElementById('input').value;
    const spinner = document.getElementById('loading-spinner');
    const output = document.getElementById('output');
    const searchResults = document.getElementById('search-results');

    // Clear previous output and show spinner
    output.innerHTML = '';
    searchResults.innerHTML = '';
    spinner.style.display = 'block';

    try {
        // Fetching notes using the new endpoint
        const response = await fetch('/generate-notes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: inputText }),
        });

        // Check if the response is okay
        if (!response.ok) throw new Error(`Error: ${response.statusText}`);

        const notesData = await response.json();
        output.innerHTML = `<strong>Notes:</strong> ${notesData.notes}<br><br>`;

        // Fetching Google search results
        const searchResponse = await fetch('/search-google', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: inputText }),
        });

        // Check if the search response is okay
        if (!searchResponse.ok) throw new Error(`Error: ${searchResponse.statusText}`);

        const searchData = await searchResponse.json();

        // Build HTML for search results
        const searchResultsHtml = searchData.results.map(result => {
            return `
                <div class="search-result">
                    <strong>${result.title}</strong><br>
                    <a href="${result.link}" target="_blank">${result.link}</a><br>
                    <div class="snippet">${result.snippet}</div>
                </div><br>
            `;
        }).join('');

        searchResults.innerHTML = `<strong>Search Results:</strong><br>${searchResultsHtml}`;

    } catch (error) {
        // Display error message if something goes wrong
        output.innerHTML = `<strong>Error:</strong> ${error.message}`;
    } finally {
        // Hide spinner after processing is complete
        spinner.style.display = 'none';
    }
});


