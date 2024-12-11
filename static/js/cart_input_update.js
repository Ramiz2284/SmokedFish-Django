function updateQuantity(itemId, quantity) {
	const csrfToken = document.querySelector('[name="csrf-token"]').content

	fetch(`/update-cart/${itemId}/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrfToken,
		},
		body: JSON.stringify({ quantity: quantity }),
	})
		.then(response => {
			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`)
			}
			return response.json()
		})
		.then(data => {
			if (data.success) {
				// Обновляем только числовое значение
				document.getElementById(`total-item-${itemId}`).textContent =
					data.item_total_price
				document.getElementById('total-price').textContent = data.total_price
			} else {
				alert(data.message)
			}
		})
		.catch(error => {
			console.error('Error updating quantity:', error)
		})
}

function removeFromCart(cartItemId) {
	const csrfToken = document.querySelector('[name="csrf-token"]').content

	fetch(`/remove-from-cart/${cartItemId}/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrfToken,
		},
	})
		.then(response => response.json())
		.then(data => {
			if (data.success) {
				// Удаляем строку элемента из таблицы
				document
					.querySelector(`input[name="quantity_${cartItemId}"]`)
					.closest('tr')
					.remove()

				// Обновляем общую стоимость корзины
				document.getElementById(
					'total-price'
				).textContent = `${data.total_price} tl`

				alert('{% trans "Item removed successfully!" %}')
			} else {
				alert(data.message)
			}
		})
		.catch(error => {
			console.error('Error removing item:', error)
			alert('{% trans "Something went wrong!" %}')
		})
}

function clearCart() {
	const csrfToken = document.querySelector('[name="csrf-token"]').content

	fetch(`/clear-cart/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrfToken,
		},
	})
		.then(response => response.json())
		.then(data => {
			if (data.success) {
				// Очистить таблицу корзины
				const cartTable = document.querySelector('.table tbody')
				if (cartTable) {
					cartTable.innerHTML = ''
				}

				// Обновить общую стоимость
				document.getElementById('total-price').textContent = '0 tl'

				alert('{% trans "Cart cleared successfully!" %}')
			} else {
				alert(data.message)
			}
		})
		.catch(error => {
			console.error('Error clearing cart:', error)
			alert('{% trans "Something went wrong while clearing the cart!" %}')
		})
}
