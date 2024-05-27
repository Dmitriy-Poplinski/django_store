$(".plus-cart").click(function() {
    let id = $(this).data("pid")
    let el = this.parentNode.children[2]

    $.ajax({
        type: "GET",
        url: "/plus-cart",
        data: {
            product_id: id
        },
        success: function (data) {
            el.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("total_amount").innerText = "$ " + data.total_amount
        }
    })
})

$(".minus-cart").click(function() {
    let id = $(this).data("pid")
    let el = this.parentNode.children[2]

    $.ajax({
        type: "GET",
        url: "/minus-cart",
        data: {
            product_id: id
        },
        success: function (data){
            el.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("total_amount").innerText = "$ " + data.total_amount
        }
    })
})

$(".remove-cart").click(function() {
    let id = $(this).data("pid")
    let el = $(this).closest(".row")

    $.ajax({
        type: "GET",
        url: "/remove-cart",
        data: {
            product_id: id
        },
        success: function (data) {
            document.getElementById("amount").innerText = data.amount
            document.getElementById("total_amount").innerText = "$ " + data.total_amount
            el.remove()
        }
    })
})

$('input[type=radio][name=customer_id]').change(function() {
    $('#selected_customer_id').val($(this).val());
});

$(".plus-wishlist").click(function() {
    let id = $(this).data("pid").toString()

    $.ajax({
        type: "GET",
        url: "/plus-wishlist",
        data: {
            product_id: id
        },
        success: function() {
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})

$(".minus-wishlist").click(function() {
    let id = $(this).data("pid").toString()

    $.ajax({
        type: "GET",
        url: "/minus-wishlist",
        data: {
            product_id: id
        },
        success: function() {
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})
