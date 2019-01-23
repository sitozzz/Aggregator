function boxberryOrder(boxberryData) {
    console.log(boxberryData);

    boxberryData[0].shippingPoints.forEach(element => {
        var root = d.getElementById('boxberry-dropdown-from');
        var option = d.createElement('option');
        option.id = element['Code'];
        option.innerText = element['Name'];
        option.value = element['Name'];
        root.appendChild(option);
    });

    if (deliveryDataTo != 'door') {
        boxberryData[0].receptionPoints.forEach(element => {
            var root = d.getElementById('boxberry-dropdown-to');
            var option = d.createElement('option');
            option.id = element['Code'];
            option.innerText = element['AddressReduce'];
            option.value = element['Address'];
            root.appendChild(option);
        });

        $("#reciever-door-boxberry").hide();
        $("#coment-boxberry").hide();
        $("#reciever-warehouse-boxberry").show();
    } else {
        boxberryData[0].receptionPoints.forEach(element => {
            var root = d.getElementById('boxberry-zip-to');
            var option = d.createElement('option');
            option.id = element['Zip'];
            option.innerText = element['Zip'];
            option.value = element['Zip'];
            root.appendChild(option);
        });

        $("#reciever-warehouse-boxberry").hide();
        $("#coment-boxberry").show();
        $("#reciever-door-boxberry").show();
    }

    $('#calc').fadeOut('fast', function () {
        $("#sender-city-boxberry").val($('#city1').val().split(',')[0]);
        $("#sender-city-boxberry").attr('disabled', true);
        $("#reciever-warehouse-city-boxberry").val($('#city2').val().split(',')[0]);
        $("#reciever-warehouse-city-boxberry").attr('disabled', true);
        prepareKladrAutocomplete('reciever-city-boxberry', 'reciever-street-boxberry', 'reciever-house-boxberry', 'reciever-address-boxberry', 'city2');
        $('#boxberry-order').fadeIn('fast');
    });
}

function addDeliveryBoxberry() {
    var sender = {
        'code' : $("#boxberry-dropdown-from option:selected").attr('id')
        // 'phone': $('#sender-phone-boxberry').val(),
        // 'name': $('#sender-name-boxberry').val()
    };

    var reciever = {
        'nameCity' : $('#city2').val(),
        'phone': $('#reciever-phone-boxberry').val(),
        'name': $('#reciever-name-boxberry').val()
    };

    email = $('#reciever-email-boxberry').val();

    if (email != '') {
        reciever['email'] = $('#reciever-email-boxberry').val();
    }

    var package = {
        'height': $('#height').val(),
        'width': $('#width').val(),
        'weight': $('#weight').val(),
        'length': $('#length').val()
    };

    if (deliveryDataTo != 'door') {
        reciever['code'] = $("#boxberry-dropdown-to option:selected").attr('id');
    } else {
        reciever['zip'] = $("#boxberry-dropdown-to option:selected").attr('id');
        reciever['street'] = $('#reciever-street-boxberry').val();
        reciever['flat'] = $('#reciever-house-boxberry').val();
        reciever['house'] = $('#reciever-flat-boxberry').val();
        coment = $('#reciever-coment-boxberry').val();

        if (coment != '') {
            reciever['coment'] = $('#reciever-coment-boxberry').val();
        }
    }
    console.log(reciever);
    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: "/boxberry_delivery",
        data: JSON.stringify({
            'sender': sender,
            'reciever': reciever,
            'package': package
        }),
        success: function (response) {
            console.log(response);
            var result = response['boxberryInfoOrder'];

            if ('track' in result) {
                alert(`Трекинг код для посылки: ${result['track']}`);
            } else if ('err' in result) {
                alert(`Ошибка: ${result['err']}`);
            } else {
                alert('Не удалось сформировать заказ');
            }
        }
    });
}

$(document).ready(function(){
    $("#close-boxberry-order").click(function () {
        $("#boxberry-order").fadeOut('fast', function () { $("#calc").fadeIn('fast'); });
        $("#shipping-offers").show();
    });

    $('#boxberry-order-btn').click(function () { 
        addDeliveryBoxberry();
    });
})