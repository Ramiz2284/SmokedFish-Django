;(function waitForJQuery() {
	if (typeof django !== 'undefined' && django.jQuery) {
		var $ = django.jQuery

		$(document).ready(function () {
			console.log('parler.js loaded and executed with jQuery')
			// Ваш основной код
			$('.parler-language-tabs').each(function () {
				var $this = $(this)
				$this.find('.language-choice').click(function (e) {
					e.preventDefault()
					var language = $(this).data('language')
					$this.find('.language-choice').removeClass('active')
					$(this).addClass('active')

					var fieldset = $this.closest('fieldset')
					fieldset.find('.parler-language-field').hide()
					fieldset
						.find('.parler-language-field[data-language="' + language + '"]')
						.show()
				})
			})

			$('.parler-language-tabs .language-choice:first-child').trigger('click')
		})
	} else {
		console.log('Waiting for django.jQuery...')
		setTimeout(waitForJQuery, 100) // Повторная проверка через 100ms
	}
})()
