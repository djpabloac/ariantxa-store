let updateBtns = document.getElementsByClassName("update-cart")

for (let index = 0; index < updateBtns.length; index++) {
    updateBtns[index].addEventListener("click", function(){
        const productId = this.dataset.product
        const action = this.dataset.action

        if(user == "AnonymousUser"){
            console.log("Not logged in")
        } else{
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action){
    const url = "/update_item/"

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            'productId': productId, 
            'action': action
        })
    }).then((response) => {
        return response.json()
    }).then((data) => {
        location.reload()
    })
}