document.addEventListener('DOMContentLoaded', function () {
	// Вы можете получить текущее значение количества товаров в корзине через API или шаблон.
	const cartCountElement = document.getElementById('cart-count')
	if (cartCountElement) {
		const initialCount = cartCountElement.textContent || 0
		updateCartCount(initialCount)
	}
})

function updateCartCount(count) {
	const cartCountElement = document.getElementById('cart-count')
	if (cartCountElement) {
		cartCountElement.textContent = count
	}
}
