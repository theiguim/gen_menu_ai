document.addEventListener("DOMContentLoaded", () => {

    // fetching backend menu data
    fetch('/results_data')
        .then(response => response.json())
        .then(data => {
            const results = data.results;
            const resultList = document.getElementById("result-list");


            results.forEach(item => {

                const result = JSON.parse(item);

                result.forEach(itn => {

                    const listItem = document.createElement("div");
                    listItem.classList.add("elements")

                    const title = document.createElement("h1");
                    title.textContent = itn.title || "Title not available";


                    const description = document.createElement("p");
                    description.textContent = itn.description || "Description not available";


                    const price = document.createElement("h2");
                    price.textContent = itn.price ? `Price: ${itn.price}` : "Price not available";


                    listItem.appendChild(title);
                    listItem.appendChild(description);
                    listItem.appendChild(price);

                    resultList.appendChild(listItem);
                })

            });
        })
        .catch(error => console.error("Fething results error:", error));

});