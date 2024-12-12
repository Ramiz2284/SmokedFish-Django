document.addEventListener('DOMContentLoaded', function () {
	// Функция добавления товара в корзину
	window.addToCart = function (productId, event) {
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
					const cartIcon = document.querySelector('.fa-shopping-cart')
					const button = event.target // Используем событие для получения кнопки
					const buttonRect = button.getBoundingClientRect() // Получаем координаты кнопки
					const cartRect = cartIcon.getBoundingClientRect() // Получаем координаты корзины

					// Создаем клон кнопки
					const productClone = button.cloneNode(true)
					document.body.appendChild(productClone)

					// Устанавливаем начальное положение клонированной кнопки
					productClone.style.position = 'absolute'
					productClone.style.left = `${buttonRect.left + window.pageXOffset}px`
					productClone.style.top = `${buttonRect.top + window.pageYOffset}px`
					productClone.style.transition =
						'transform 0.8s ease-in-out, opacity 0.8s ease-in-out'
					productClone.style.zIndex = 9999

					// Вычисляем конечное положение корзины
					const deltaX = cartRect.left - buttonRect.left
					const deltaY = cartRect.top - buttonRect.top

					// Добавляем анимацию
					setTimeout(() => {
						productClone.style.transform = `translate(${deltaX}px, ${deltaY}px) scale(0.5)`
						productClone.style.opacity = '0'
					}, 50)

					// Удаляем клон после анимации
					setTimeout(() => {
						productClone.remove()
					}, 850)

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
