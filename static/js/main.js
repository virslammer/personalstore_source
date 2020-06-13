

/* 

	1. Add to cart

*/
function getCookie(name) {
	var cookieArr = document.cookie.split(";");
	for (var i=0; i< cookieArr.length; i++) {
		var cookiePair = cookieArr[i].split("=");

		if (name == cookiePair[0].trim()) {

			return decodeURIComponent(cookiePair[1])
		}
	}
	return null;
}

let cart = JSON.parse(getCookie('cart'))

if (cart == undefined) {
	cart = {};
	console.log('cart created ', cart);
	document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/"
}

let updateBtns = document.getElementsByClassName('update-cart')

for (var i of updateBtns) {
	i.addEventListener('click', function() {
		
		var productId = this.dataset.product
        var action = this.dataset.action 
        var quantity = 1
		if (document.getElementById("quantity_input")) {
			quantity = document.getElementById("quantity_input").value;
		}
		addCookieItem(productId,action,quantity)
	})
}


function addCookieItem(productId, action,quantity) {
	if (action =='add') {
		if (cart[productId] == undefined){
			cart[productId] = { 'quantity':parseInt(quantity)}
		} else {
			cart[productId]['quantity'] = parseInt(cart[productId]['quantity']) + parseInt(quantity)
		}
	}
	if (action =='remove') {
		cart[productId]['quantity'] -= 1
		if (cart[productId]['quantity'] <= 0){
			console.log('removed item')
			delete cart[productId]
		} 
	}
	if (action == 'clear') {
		console.log(cart)
		cart = {}
	}
	document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
	$('#cart').load(document.URL +  ' #cart');
	if (document.getElementById('cart_detail')) {
		location.reload(true)
	}
	
}



// function updateUserOrder(productId, action) {
// 	var url = '/update-item/'

// 	fetch(url, {
// 		method:'POST',
// 		headers:{
// 			'Content-Type': 'application/json',
// 			'X-CSRFToken':csrftoken,
// 		},
// 		body:JSON.stringify({'productId':productId, 'action':action})
// 	})
// 	.then((response) => {
// 		return response.json()
// 	})
// 	.then((data) => {
// 		console.log('data:',data)
// 		location.reload(true)
// 	})
// }

function refreshPage () {
	var page_y = document.getElementsByTagName("body")[0].scrollTop;
	window.location.href = window.location.href.split('?')[0] + '?page_y=' + page_y;
}


/* 

	2. Sorting products

*/
// let sorting_btn = document.getElementsByClassName('product_sorting_btn')
// sorting_btn.addEventListener('click', function() {
// 	var sort_type = this.dataset.sorting;
// 	var category_id = this.dataset.category;
// 	var url = '/category/' +category_id;
// 	console.log(sort_type)
// 	fetch(url, {
// 				method:'POST',
// 				headers:{
// 					'Content-Type': 'application/json',
// 					'X-CSRFToken':csrftoken,
// 				},
// 				body:JSON.stringify({'sort':sort_type})
// 			})
// 			.then((response) => {
// 				return response.json()
// 			})
// 			.then((data) => {
// 				console.log('data:',data)
// 				location.reload(true)
// 			})

// })