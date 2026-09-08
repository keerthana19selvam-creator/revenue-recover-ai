const API_URL = "https://revenue-recover-ai-1-1c4i.onrender.com";

// --------------------------------------------------
// LOAD PAYMENTS
// --------------------------------------------------

async function loadPayments() {

    try {

        const response = await fetch(`${API_URL}/payments`);

        if (!response.ok) {
            throw new Error("Failed to load payments");
        }

        const payments = await response.json();

        console.log("Payments received:", payments);

        displayPayments(payments);

    } catch (error) {

        console.error("Backend connection failed:", error);

    }
}


// --------------------------------------------------
// DISPLAY PAYMENTS
// --------------------------------------------------

function displayPayments(payments) {

    const container = document.getElementById("payments-container");

    if (!container) {
        console.log("payments-container not found");
        return;
    }

    container.innerHTML = "";

    payments.forEach(payment => {

        const card = document.createElement("div");

        card.className = "payment-card";

        card.innerHTML = `
            <h3>Payment ID: ${payment.id}</h3>

            <p>
                Customer: ${payment.customer}
            </p>

            <p>
                Amount: ₹${Number(payment.amount).toLocaleString("en-IN")}
            </p>

            <p>
                Status: ${payment.status}
            </p>

            <p>
                Recovery Probability:
                ${payment.recovery_probability}%
            </p>

            <p>
                Recommended Action:
                ${payment.recommended_action}
            </p>

            <button onclick="analyzePayment('${payment.id}')">
                Analyze Payment
            </button>
        `;

        container.appendChild(card);
    });
}


// --------------------------------------------------
// ANALYZE PAYMENT USING ML
// --------------------------------------------------

async function analyzePayment(paymentId) {

    console.log("Analyzing:", paymentId);

    try {

        // Get payment data
        const response = await fetch(`${API_URL}/payments`);

        const payments = await response.json();

        const payment = payments.find(
            p => p.id === paymentId
        );

        if (!payment) {
            alert("Payment not found!");
            return;
        }


        // Convert payment information into 3 ML features
        const features = [
            payment.amount,
            payment.status === "Failed" ? 1 : 0,
            payment.recovery_probability
        ];


        console.log("Features sent to ML:", features);


        // Send features to Flask
        const predictionResponse = await fetch(
            `${API_URL}/predict`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    features: features
                })
            }
        );


        const result = await predictionResponse.json();

        console.log("ML Result:", result);


        if (!predictionResponse.ok || !result.success) {

            throw new Error(
                result.error || "Prediction failed"
            );
        }


        // Show result
        alert(
            `🤖 AI Payment Analysis\n\n` +
            `Payment ID: ${payment.id}\n` +
            `Customer: ${payment.customer}\n` +
            `Amount: ₹${payment.amount}\n\n` +
            `AI Prediction: ${result.prediction}\n\n` +
            `Recommended Action:\n${payment.recommended_action}`
        );


    } catch (error) {

        console.error("Analysis failed:", error);

        alert(
            "❌ Payment analysis failed.\n\n" +
            error.message
        );
    }
}


// --------------------------------------------------
// START
// --------------------------------------------------

loadPayments();
