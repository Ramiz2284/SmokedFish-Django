document.addEventListener('DOMContentLoaded', function () {
	// Функция добавления товара в корзину
	window.addToCart = function (productId) {
		const csrfToken = document.querySelector('[name="csrf-token"]').content

		fetch(`/add-to-cart/${productId}/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrfToken,
			},
			body: JSON.stringify({ product_id: productId }),
		})
			.then(response => response.json())
			.then(data => {
				if (data.success) {
					alert('Product added to cart!')
					// Обновляем количество товаров в корзине
					const cartCountElement = document.getElementById('cart-count')
					if (cartCountElement) {
						cartCountElement.textContent = data.cart_count
					}
				} else {
					alert(data.message)
				}
			})
			.catch(error => {
				console.error('Fetch error:', error)
				alert('Something went wrong! Please try again later.')
			})
	}
})
