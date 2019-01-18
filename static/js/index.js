// Название перевозщика
// Звезды
// Дата отправки
// Дата приема 
// Цена 
// function showResults(data) {
//     data = [
//         {
//             name: 'sdek',
//             shippingDate: '21',
//             receivingDate: '23',
//             price: 2767,
//         },
//         {
//             name: 'dek',
//             shippingDate: '23',
//             receivingDate: '23',
//             price: 27267,
//         },
//         {
//             name: 'mek',
//             shippingDate: '23',
//             receivingDate: '27',
//             price: 27167,
//         }
//     ]
//     for (const carrier of data) {
//         showCarrier(carrier)
//     }
// }

// function showCarrier({name, shippingDate, receivingDate, price}) {
//     const container = d.createElement('div')
//     container.setAttribute('class', 'carrier')
    
//     const nameElement  = d.createElement('div')
//     nameElement.setAttribute('class', 'carrier-name')
//     nameElement.textContent = name

//     const shippingDateElement  = d.createElement('div')
//     shippingDateElement.setAttribute('class', 'carrier-shipping-date')
//     shippingDateElement.textContent = shippingDate

//     const receivingDateElement  = d.createElement('div')
//     receivingDateElement.setAttribute('class', 'carrier-receiving-date')
//     receivingDateElement.textContent = receivingDate

//     const priceElement  = d.createElement('div')
//     priceElement.setAttribute('class', 'carrier-price')
//     priceElement.textContent = price

//     container.appendChild(nameElement)
//     container.appendChild(shippingDateElement)
//     container.appendChild(receivingDateElement)
//     container.appendChild(priceElement)

//     d.getElementById('shipping-offers').appendChild(container)
// }
var city1;
var city2;
var deliveryDataFrom = 'door';
var deliveryDataTo = 'door';
var d = document;

function* entries(obj) {
    for (let key of Object.keys(obj)) {
        yield [key, obj[key]];
    }
}

//This sends to server
//City object
function City(id, name) {
    this._id = id;
    this._name = name;
}
//Delivery data
function DeliveryData(weight, length, height, width, size) {
    if (size == undefined) {
        this.weight = weight;
        this.length = length;
        this.height = height;
        this.width = width;
    } else {
        this.weight = weight;
        this.size = size;
    }
}


function showResults(data) {
    showDPDres(data.dpd);
    showPonyres(data.pony);
    showBoxberry(data.boxberry);
    showSDEKres(data.sdek);
}

function showDPDres(dpdData) {
    $('#dpd-output').html('');
    if (dpdData[0].serviceName) {
        var dpdHolder = d.getElementById('dpd-output');
        var row = d.createElement('div')
        row.className = 'row';
        row.style = "margin:auto; padding:0; max-width: 600px; padding: 24px;border: 1px solid gray; border-radius: 15px;";
        dpdHolder.appendChild(row);
        var title = d.createElement('h1');
        title.innerText = 'Стоимость доставки DPD';
        row.appendChild(title);
        for (let r in dpdData) {
            var propHolder = d.createElement('div');
            propHolder.style = 'width:100%;';
            propHolder.innerHTML = '<p> услуга: ' + dpdData[r].serviceName + ', цена: ' + dpdData[r].cost + ' дней до доставки: ' + dpdData[r].days + '</p>'
            row.appendChild(propHolder);
        }
    } else {
        var dpdHolder = d.getElementById('dpd-output');
        var row = d.createElement('div')
        row.className = 'row';
        row.style = "margin:auto; padding:0; max-width: 600px; padding: 24px;border: 1px solid gray; border-radius: 15px;";
        dpdHolder.appendChild(row);
        var title = d.createElement('h1');
        title.innerText = dpdData.replace('Server raised fault: ', '');
        row.appendChild(title);

    }

    $('#dpd-output').show();
}
function showPonyres(ponyData) {
    $('#pony-output').html('');
    $('#pony-output').show();
    let row = d.createElement('div')
    let title = d.createElement('h1');
    title.innerText = 'Pony Express';
    row.appendChild(title);
    row.className = 'row';
    row.style = "margin:auto; padding:0; max-width: 600px; padding: 24px;border: 1px solid gray; border-radius: 15px;";



    for (let i in ponyData) {

        var propHolder = d.createElement('div');
        propHolder.style = 'width:100%;';
        propHolder.innerHTML = '<p> услуга: ' + ponyData[i].Mode + ', цена без НДС: ' + ponyData[i].Sum + ' НДС: ' + ponyData[i].VAT + ' дней до доставки: ' + ponyData[i].MaxTerm + '</p>'
        row.appendChild(propHolder);
    }
    $('#pony-output').append(row);
    //----------------------------------------




}

$(document).ready(function () {
    d.getElementById('dateExecute').value = new Date().toISOString().slice(0, 10);
    $('input[name=fromDelivery]').on('change', function () {
        deliveryDataFrom = $(this).val();
    });
    $('input[name=toDelivery]').on('change', function () {
        deliveryDataTo = $(this).val();
    });
    $('input[name=calcVariant]').on('change', function () {
        if ($(this).val() == 'variant1') {
            $('#variant1').show();
            $('#variant2').hide();
        } else {
            $('#variant1').hide();
            $('#variant2').show();
        }

    });
    $("#city1").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: "http://api.cdek.ru/city/getListByTerm/jsonp.php?callback=?",
                dataType: "jsonp",
                data: {
                    q: function () {
                        return $("#city1").val()
                    },
                    name_startsWith: function () {
                        return $("#city1").val()
                    }
                },
                success: function (data) {
                    console.log('RESPONSE:');
                    console.log(data);
                    response($.map(data.geonames, function (item) {
                        return {
                            label: item.name,
                            value: item.name,
                            id: item.id
                        }
                    }));
                }
            });
        },
        minLength: 1,
        select: function (event, ui) {
            city1 = new City(ui.item.id, ui.item.value);
        }
    });
    $("#city2").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: "http://api.cdek.ru/city/getListByTerm/jsonp.php?callback=?",
                dataType: "jsonp",
                data: {
                    q: function () {
                        return $("#city2").val()
                    },
                    name_startsWith: function () {
                        return $("#city2").val()
                    }
                },
                success: function (data) {
                    console.log('RESPONSE:');
                    console.log(data);
                    response($.map(data.geonames, function (item) {
                        return {
                            label: item.name,
                            value: item.name,
                            id: item.id
                        }
                    }));
                }
            });
        },
        minLength: 1,
        select: function (event, ui) {
            city2 = new City(ui.item.id, ui.item.value);
        }
    });
    $("#calcBtn1").click(function () {
        $("#prop-holder").show(100);
    });
    $("#calcBtn").click(function () {

        //Collect data from fields
        let size;
        if ($('#variant2').is(':visible')) {
            size = $('#size').val();
        }
        let deliveryData = new DeliveryData(

            $('#weight').val(),
            $('#length').val(),
            $('#height').val(),
            $('#width').val(),
            size
        );
        console.log('Delivery data = ');
        console.log(deliveryData);

        // TODO: Show loader here!
        $('#loader').show();
        $.ajax({
            url: "/calculate",
            contentType: 'application/json',
            method: 'POST',
            data: JSON.stringify({
                'city1': {
                    'id': city1._id,
                    'name': city1._name,
                },
                'city2': {
                    'id': city2._id,
                    'name': city2._name,
                },
                'dateExecute': $('#dateExecute').val(),
                // 'tariffName': $('#tariff').find(':selected').text(),

                //Door to door, door to storage and other 
                'deliveryType': {
                    'deliveryFrom': deliveryDataFrom,
                    'deliveryTo': deliveryDataTo
                },

                //TODO: Example hardcode!!!
                'goods': [
                    {
                        'weight': deliveryData.weight,
                        'height': deliveryData.height,
                        'width': deliveryData.width,
                        'length': deliveryData.length,
                        'volume': deliveryData.size
                    }
                ]
            }),
            success: function (data) {
                // TODO: Hide loader here!
                $('#loader').hide();
                console.log(data);

                showResults(data)

                $('#output').show('fast');
            }
        });
    });
    $("#close-sdek-order").click(function () {
        $("#order").fadeOut('fast', function () { $("#calc").fadeIn('fast'); });
    });

    $('#sdekOrderBtn').click(function () { 
        // TODO: check this flags after user selection
        console.log('sdek delivery clicked');
        addSDEKDelivery(false, false);
        
    });

    $("#close-boxberry-order").click(function () {
        $("#boxberry-order").fadeOut('fast', function () { $("#calc").fadeIn('fast'); });
    });

    $('#boxberry-order-btn').click(function () { 
        addDeliveryBoxberry();
    });
});
