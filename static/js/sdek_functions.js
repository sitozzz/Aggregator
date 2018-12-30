// ===SDEK FUNCTIONS===
function showSDEKres(sdekdata) {
    console.log('sdek data');
    console.log(sdekdata);
    $('#sdek-output').html('');
    let tariff_map = {
        136: 'Посылка',
        137: 'Посылка',
        138: 'Посылка',
        139: 'Посылка',
        233: 'Экономичная посылка',
        234: 'Экономичная посылка',
        291: 'Express',
        293: 'Express',
        294: 'Express',
        295: 'Express',
        1: 'Экспресс лайт',
        5: 'Экономичный экспресс',
        3: 'Супер-экспресс до 18',
        10: 'Экспресс лайт',
        11: 'Экспресс лайт',
        12: 'Экспресс лайт',
        15: 'Экспресс тяжеловесы',
        16: 'Экспресс тяжеловесы',
        17: 'Экспресс тяжеловесы',
        18: 'Экспресс тяжеловесы',
        62: 'Магистральный экспресс',
        63: 'Магистральный экспресс',
    };
    if (sdekdata.error == undefined) {
        data = sdekdata.result;
        console.log(data);
        if (data != undefined) {
            let price = data['price'];
            let deliveryPeriodMin = data['deliveryPeriodMin'];
            let deliveryPeriodMax = data['deliveryPeriodMax'];
            let deliveryDateMin = data['deliveryDateMin'];
            let deliveryDateMax = data['deliveryDateMax'];
            let tariffName = data['tariffId'];
            for (let [key, value] of entries(tariff_map)) {
                if (key == tariffName) {
                    tariffName = value;
                }
            }
            var sdekHolder = d.getElementById('sdek-output');
            var row = d.createElement('div');
            row.className = 'row';
            row.style = "margin:auto; padding:0; max-width: 600px; padding: 24px;border: 1px solid gray; border-radius: 15px;";
            sdekHolder.appendChild(row);
            var title = d.createElement('h1');
            title.innerText = 'SDEK';
            row.appendChild(title);
            var propHolder = d.createElement('div');
            propHolder.style = 'width:100%';
            propHolder.innerHTML = '<p>' + price + ' Rub </p><p>Дата доставки: ' + deliveryDateMax + '</p><p>Тариф: ' + tariffName + '</p>';
            row.appendChild(propHolder);
            var btn = d.createElement('button');
            btn.className = 'btn btn-lg btn-success';
            btn.innerText = 'Заказать';
            row.appendChild(btn);
            btn.onclick = function () {
                if (deliveryDataFrom != 'door') {
                    $("#send-door").hide();
                    $("#send-storage").show();
                    getSDEKPvz(city1._id, 'sdek-dropdown-from');
                    // TODO: display full address in p tag
                }
                if (deliveryDataTo != 'door') {
                    $("#recieve-door").hide();
                    $("#recieve-storage").show();
                    getSDEKPvz(city2._id, 'sdek-dropdown-to');
                    // TODO: display full address in p tag
                }
                $('.section').fadeOut('fast', function () {
                    d.getElementById('send-city').innerText = $('#city1').val();
                    d.getElementById('recieve-city').innerText = $('#city2').val();
                    $('#order').fadeIn('fast');
                });
            };
            // var dropdownContainer = d.createElement('div');
            // dropdownContainer.id = 'drop-container';
            // dropdownContainer.style = 'display:none';
            // dropdownContainer.className = '';
            // var dropdownTo = d.createElement('select');
            // dropdownTo.id = 'sdek-dropdown-to';
            // dropdownTo.className = 'form-control';
            // var dropdownLabelTo = d.createElement('p');
            // dropdownLabelTo.innerText = 'Выберите пункт отправления из списка: ';
            // dropdownContainer.appendChild(dropdownLabelTo);
            // dropdownContainer.appendChild(dropdownTo);
            // var dropdown = d.createElement('select');
            // dropdown.id = 'sdek-dropdown';
            // dropdown.className = 'form-control';
            // var dropdownLabel = d.createElement('p');
            // dropdownLabel.innerText = 'Выберите пункт получения из списка: ';
            // dropdownContainer.appendChild(dropdownLabel);
            // dropdownContainer.appendChild(dropdown);
            // row.appendChild(dropdownContainer);
            // var fullAddressText = d.createElement('p');
            // fullAddressText.id = 'full-address-text';
            // row.appendChild(fullAddressText);
            $(sdekHolder).show();
        }
    }
}
function getSDEKPvz(city_code, rootElement) {
    console.log('CITY CODE  = ' + city_code);
    $.ajax({
        contentType: 'application/json',
        method: 'POST',
        url: "/sdek_pvz",
        data: JSON.stringify({
            "city_code": city_code
        }),
        success: function (response) {
            //TODO: Display dropdown and some info here
            console.log('Success sdek pvz');
            console.log(response);
            for (let elem in response) {
                createSDEKDropdown(response[elem], rootElement);
            }
            $('#drop-container').show();
            // $('#sdek-dropdown').on('change', function (e) {
            //    d.getElementById('full-address-text').innerText = 'Адрес ПВЗ получателя: ' + $('option:selected', this).val();
            // });
        },
        error: function (err) {
            console.log('AJAX ERROR');
            console.log(err);
        }
    });
}
function createSDEKDropdown(data, rootElement) {
    var root = d.getElementById(rootElement);
    var option = d.createElement('option');
    option.id = data['code'];
    option.innerText = data['display_name'];
    option.value = data['full_address'];
    root.appendChild(option);
}
function addSDEKDelivery(isSendStorage, isRecieveStorage) {
    var dateDelivery = new Date().toJSON().slice(0, 10);
    var sender = {
        'city_id': city1._id,
        'phone': $('#send-phone').text(),
        'name': $('#send-name').text()
    };
    var reciever = {
        'city_id': city2._id,
        'phone': $('#reciever-phone').text(),
        'name': $('#reciever-name').text()
    };
    var package = {
        'height': $('#height').val(),
        'width': $('#width').val(),
        'weight': $('#weight').val(),
        'length': $('#length').val()
    };
    if (isSendStorage) {
        // TODO: Add fields for storage
    }
    else {
        sender['street'] = $('#send-street').text();
        sender['flat'] = $('#send-flat').text();
        sender['house'] = $('#send-house').text();
    }
    if (isRecieveStorage) {
        // TODO: Add fields for storage
    }
    else {
        reciever['street'] = $('#recieve-street').text();
        reciever['flat'] = $('#recieve-flat').text();
        reciever['house'] = $('#recieve-house').text();
    }
    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: "/sdek_delivery",
        data: JSON.stringify({
            'date': dateDelivery,
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
