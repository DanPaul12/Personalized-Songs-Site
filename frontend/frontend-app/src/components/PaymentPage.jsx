import React, { useState, useEffect } from "react";
import { loadStripe } from "@stripe/stripe-js";
import { Elements, CardElement, useStripe, useElements } from "@stripe/react-stripe-js";
import axios from "axios";
import './PaymentPage.css'
import { useLocation } from "react-router-dom";

// Load Stripe instance with environment variable
const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY || '');

function PaymentForm() {
    const stripe = useStripe();
    const elements = useElements();
    const location = useLocation();

    // Extract query parameters
    const queryParams = new URLSearchParams(location.search);
    const emailFromQuery = queryParams.get("email") || "";
    const priceFromQuery = queryParams.get("price") || 0;
    const orderIdFromQuery = queryParams.get("order_id"); // Pass order_id in the query string

    // States
    const [email] = useState(emailFromQuery); // Email is pre-filled and uneditable
    const [amount] = useState(priceFromQuery); // Amount is pre-filled and uneditable
    const [songDetails, setSongDetails] = useState(""); // Dynamic song details
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");
    const [isFetchingDetails, setIsFetchingDetails] = useState(true);

    useEffect(() => {
        // Fetch song details using the order_id
        async function fetchSongDetails() {
            if (!orderIdFromQuery) {
                setMessage("Order ID is missing in the URL.");
                setIsFetchingDetails(false);
                return;
            }

            try {
                const response = await axios.get(
                    `https://api.dananddrumpersonalizedsongs.com/api/song-submissions/${orderIdFromQuery}`
                    /*`http://127.0.0.1:5000/api/song-submissions/${orderIdFromQuery}`*/
                );
                setSongDetails(response.data.song_details); // Update state with song details
            } catch (error) {
                setMessage("Failed to fetch song details. Please try again.");
                console.error("Error fetching song details:", error);
            } finally {
                setIsFetchingDetails(false);
            }
        }

        fetchSongDetails();
    }, [orderIdFromQuery]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage("");

        if (!stripe || !elements) {
            setMessage("Stripe is not loaded yet.");
            setLoading(false);
            return;
        }

        try {
            const response = await axios.post(
                "https://api.dananddrumpersonalizedsongs.com/checkout", {
                amount: amount * 100, // Convert to cents
                email: email,
                song_details: songDetails, // Pass song details
            });

            const clientSecret = response.data.clientSecret; // Extract the clientSecret string

            const { error } = await stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: elements.getElement(CardElement),
                    billing_details: { email },
                },
            });

            if (error) {
                setMessage(error.message);
            } else {
                setMessage("Payment successful! Thank you. A confirmation email will be sent shortly.");
            }
        } catch (error) {
            setMessage("An error occurred. Please try again.");
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    if (isFetchingDetails) {
        return <p>Loading song details...</p>;
    }

    return (
        <form onSubmit={handleSubmit} style={{ maxWidth: "400px", margin: "0 auto" }}>
            <h2>Make a Payment</h2>
            <label>
                Email:
                <input
                    type="email"
                    value={email}
                    disabled
                />
            </label>
            <br />
            <label>
                Amount (USD):
                <input
                    type="number"
                    value={amount}
                    disabled
                />
            </label>
            <br />
            <label>
                Song Details:
                <textarea
                    value={songDetails}
                    disabled
                    rows="3"
                />
            </label>
            <br />
            <label>
                Card Details:
                <CardElement />
            </label>
            <br />
            <button id='submit' type="submit" disabled={!stripe || loading}>
                {loading ? "Processing..." : "Pay"}
            </button>
            {message && <p>{message}</p>}
        </form>
    );
}

function PaymentPage() {
    return (
        <Elements stripe={stripePromise}>
            <PaymentForm />
        </Elements>
    );
}

export default PaymentPage;