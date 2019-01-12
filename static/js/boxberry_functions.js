var senderCityCodeBoxberry;
var recieverCityCodeBoxberry;

function showBoxberry(boxberryData) {
    console.log(boxberryData);
    $('#boxberry-output').html('');
    if (boxberryData.price) {
        senderCityCodeBoxberry = boxberryData['senderCity'];
        recieverCityCodeBoxberry = boxberryData['recipientCity']
        var blockBoxberry = d.getElementById('boxberry-output');
        console.log(blockBoxberry);
        var row = d.createElement('div');
        row.className = 'row';
        row.style = "margin: auto; padding: 0; max-width: 600px; padding: 24px;border: 1px solid gray; border-radius: 15px;";
        blockBoxberry.appendChild(row);
        var title = d.createElement('h1');
        title.innerText = 'Стоимость доставки Boxberry';
        row.appendChild(title);
        var deliveryInformation = d.createElement('div');
        deliveryInformation.style = 'width: 100%;';
        deliveryInformation.innerHTML = '<p> Цена: ' + boxberryData.price + '; дней до доставки: ' + boxberryData.period + '</p>';
        row.appendChild(deliveryInformation);

        var btn = d.createElement('button');
        btn.className = 'btn btn-lg btn-success';
        btn.innerText = 'Заказать';
        row.appendChild(btn);

        btn.onclick = function () {
            
            boxberryData.shippingPoints.forEach(element => {
                var root = d.getElementById('boxberry-dropdown-from');
                var option = d.createElement('option');
                option.id = element['Code'];
                option.innerText = element['Name'];
                option.value = element['Name'];
                root.appendChild(option);
            });

            if (deliveryDataTo != 'door') {
                boxberryData.receptionPoints.forEach(element => {
                    var root = d.getElementById('boxberry-dropdown-to');
                    var option = d.createElement('option');
                    option.id = element['Code'];
                    option.innerText = element['AddressReduce'];
                    option.value = element['Address'];
                    root.appendChild(option);
                });
            } else {
                boxberryData.receptionPoints.forEach(element => {
                    var root = d.getElementById('boxberry-dropdown-to');
                    var option = d.createElement('option');
                    option.id = element['Zip'];
                    option.innerText = element['Zip'];
                    option.value = element['Zip'];
                    root.appendChild(option);
                });

                $("#reciever-door-boxberry").show();
            }

            $('#calc').fadeOut('fast', function () {
                d.getElementById('sender-city-boxberry').innerText = $('#city1').val();
                d.getElementById('reciever-city-boxberry').innerText = $('#city2').val();

                $('#boxberry-order').fadeIn('fast');
            });
        };
    }

    $('#boxberry-output').show();
}

function addDeliveryBoxberry() {
    var sender = {
        'city_id': senderCityCodeBoxberry//,
        // 'phone': $('#sender-phone-boxberry').val(),
        // 'name': $('#sender-name-boxberry').val()
    };
    var reciever = {
        'city_id': recieverCityCodeBoxberry,
        'phone': $('#reciever-phone-boxberry').val(),
        'name': $('#reciever-name-boxberry').val()
    };
    var package = {
        'height': $('#height').val(),
        'width': $('#width').val(),
        'weight': $('#weight').val(),
        'length': $('#length').val()
    };
    sender['code'] = $("#boxberry-dropdown-from option:selected").attr('id');
    if (deliveryDataTo != 'door') {
        reciever['code'] = $("#boxberry-dropdown-to option:selected").attr('id');
    } else {
        reciever['zip'] = $("#boxberry-dropdown-to option:selected").attr('id');
        reciever['street'] = $('#reciever-street-boxberry').val();
        reciever['flat'] = $('#reciever-house-boxberry').val();
        reciever['house'] = $('#reciever-flat-boxberry').val();
    }
    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: "/boxberry_delivery",
        data: JSON.stringify({
            'sender': sender,
            'reciever': reciever,
            package: package
        }),
        success: function (response) {
            console.log('response = ' + response);
            console.log(response[0]);
        }
    });
}