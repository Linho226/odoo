document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('buy_now_form');
  
    form.addEventListener('submit', function (event) {
      event.preventDefault(); // Empêche la soumission classique du formulaire
  
      // Récupérer les données du formulaire
      const formData = new FormData(form);
      const productId = formData.get('product_id');
      const name = formData.get('name');
      const email = formData.get('email');
      const phone = formData.get('phone');
  
      // Créer un objet de données à envoyer au contrôleur Odoo
      const dataToSend = {
        product_id: productId,
        name: name,
        email: email,
        phone: phone
      };
  
      // Envoi des données au contrôleur Odoo via AJAX
      fetch('/buy_now/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataToSend)
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          // Rediriger vers la page de paiement CinetPay
          window.location.href = data.redirect_url;
        } else {
          alert('Erreur lors de la soumission des données');
        }
      })
      .catch(error => {
        console.error('Erreur lors de la soumission:', error);
      });
    });
  });
  