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

var cart = JSON.parse(getCookie('cart'))

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
        if (user === 'AnonymousUser') {
            console.log('not login')
            addCookieItem(productId,action)
            console.log(cart)

        } else {
            console.log(productId,action)
            updateUserOrder(productId, action)
        }
    })
}


function addCookieItem(productId, action) {
    if (action =='add') {
        if (cart[productId] == undefined){
            cart[productId] = { 'quantity':1}
        } else {
            cart[productId]['quantity'] += 1
        }
    }
    if (action =='remove') {
        cart[productId]['quantity'] -= 1
        if (cart[productId]['quantity'] <= 0){
            console.log('removed item')
            delete cart[productId]
        } 
    }
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
    location.reload()
}



function updateUserOrder(productId, action) {
    var url = '/update-item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log('data:',data)
        location.reload()
    })
}