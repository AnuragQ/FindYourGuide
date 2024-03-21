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
    const product_id = document.querySelector("#submitBtn").getAttribute("data-product-id");
    const quantity = document.getElementById("quantity").value;

    fetch(`/payment/create-checkout-session?product_id=${product_id}&quantity=${quantity}`)
    .then((result) => { return result.json(); })
    .then((data) => {
      console.log(data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  });

});