import React, { useState } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import { Elements, CardElement, useStripe, useElements } from '@stripe/react-stripe-js';
import CheckoutForm from './CheckoutForm';

const stripePromise = loadStripe('your_stripe_publishable_key');

function CheckoutForm({ amount }) {
    const stripe = useStripe();
    const elements = useElements();
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (event) => {
        event.preventDefault();
        setIsLoading(true);

        const { error, paymentIntent } = await stripe.confirmCardPayment(
            'your_client_secret_from_backend',
            {
                payment_method: {
                    card: elements.getElement(CardElement),
                },
            }
        );

        if (error) {
            console.error('Payment error:', error);
            alert('Payment failed. Please try again.');
        } else if (paymentIntent.status === 'succeeded') {
            alert('Payment successful!');
        }

        setIsLoading(false);
    };

    return (
        <form onSubmit={handleSubmit}>
            <h3>Order Total: ${amount / 100}</h3>
            <CardElement />
            <button type="submit" disabled={!stripe || isLoading}>
                {isLoading ? 'Processing...' : 'Pay Now'}
            </button>
        </form>
    );
}

function PaymentPage() {
    const amount = 10000; // Replace with the order's actual amount in cents

    return (
        <Elements stripe={stripePromise}>
            <CheckoutForm amount={amount} />
        </Elements>
    );
}

export default PaymentPage;