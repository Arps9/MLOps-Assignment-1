const form = document.getElementById("prediction-form");
const resultBox = document.getElementById("result");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const values = Object.fromEntries(new FormData(form).entries());
  for (const key of Object.keys(values)) values[key] = Number(values[key]);

  resultBox.textContent = "Predicting...";
  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(values)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Prediction failed");
    resultBox.innerHTML = `<strong>${data.species}</strong><br>Confidence: ${data.confidence}%`;
  } catch (error) {
    resultBox.textContent = `Error: ${error.message}`;
  }
});
