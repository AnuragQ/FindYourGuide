console.log("The payment script is loaded")

fetch("/payment/config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);

   // Event handler
  document.querySelector("#submitBtn").addEventListener("click", () => {
    // Get Checkout Session ID
    console.log("Submitted Go to Payment")
    const booking_id = document.querySelector("#submitBtn").getAttribute("data-booking-id");

    fetch(`/payment/create-checkout-session?booking_id=${booking_id}`)
    .then((result) => { return result.json(); })
    .then((data) => {
      if(data.error){
        alert(data.error);
        return;
      }
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  });

});