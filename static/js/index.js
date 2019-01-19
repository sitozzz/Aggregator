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

// Название перевозщика
// Звезды
// Дата отправки
// Дата приема 
// Цена 
function showResults(data) {
    data = [
        {
            name: 'cdek',
            shippingDate: 1547906646,
            receivingDate: 1547906646,
            price: 2767,
        },
        {
            name: 'dpd',
            shippingDate: 1547906646,
            receivingDate: 1547906646,
            price: 27267,
        },
    ]
    for (const carrier of data) {
        showCarrier(carrier)
    }
}

function transformDateToString(unixTimestamp) {
    const date = new Date(unixTimestamp * 1000)
    const options = { month: 'long', day: 'numeric' };
    return date.toLocaleDateString(undefined, options);
}

function transformData({name, shippingDate, receivingDate, price}) {
    const logoClassName = `carrier-logo-${name}`
    const fromText = transformDateToString(shippingDate)
    const toText = transformDateToString(receivingDate)
    const priceText = `${price}₽`

    return { logoClassName, fromText, toText, priceText }
}

function showCarrier({name, shippingDate, receivingDate, price}) {
    const container = d.createElement('div')
    container.setAttribute('class', 'carrier')
    
    const { logoClassName, fromText, toText, priceText } = transformData({ name, shippingDate, receivingDate, price })

    const nameElement  = d.createElement('div')
    nameElement.classList.add('carrier-logo', logoClassName)

    const shippingDateElement  = d.createElement('div')
    shippingDateElement.setAttribute('class', 'carrier-shipping-date')
    shippingDateElement.textContent = fromText

    const receivingDateElement  = d.createElement('div')
    receivingDateElement.setAttribute('class', 'carrier-receiving-date')
    receivingDateElement.textContent = toText

    const priceElement  = d.createElement('div')
    priceElement.setAttribute('class', 'carrier-price')
    priceElement.textContent = priceText

    container.appendChild(nameElement)
    container.appendChild(shippingDateElement)
    container.appendChild(receivingDateElement)
    container.appendChild(priceElement)
    
    const shippingOffers = d.getElementById('shipping-offers')
    shippingOffers.appendChild(container)
    shippingOffers.classList.add('shipping-offers-active')

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
            },
            error: function () {
                // TODO: Hide loader here!
                $('#loader').hide();

                showResults()

                $('#output').show('fast');
            },

            
        });
    });
    

});