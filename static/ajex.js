$(document).ready(function(){
    $(".add-to-cart").click(function(){
        var _index = $(this).attr('data-index');
        var _qty = $(".product-qty-"+_index).val();
        let qty = parseInt(_qty);
        console.log(qty);
        if(qty <= 0){
            window.alert("enter the valid quatity");
            return;
        }
        var _productId = $(".product-id-"+_index).val();
        var _productTitle = $(".product-title-"+_index).val();
        var _productPrice = $(".product-price-"+_index).text();
        var _productImage = $(".product-image-"+_index).val();
        $.ajax({
            url:'add-to-cart',
            type:'GET',
            dataType:'json',
            data:{
                'id':_productId,
                'title':_productTitle,
                'price':_productPrice,
                'qty':_qty,
                'image':_productImage,
            },
            success:function(response){
                $(".cart-list").text(response.totalitems);
            }

        });
   });

 });

 