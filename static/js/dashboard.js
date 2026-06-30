document.querySelectorAll("canvas[id^='chart']").forEach(canvas=>{
    const tanggal = JSON.parse(canvas.dataset.tanggal);
    const harga = JSON.parse(canvas.dataset.harga);
    const status = canvas.dataset.status;

    let borderColor;
    let backgroundColor;

    if (status === "naik") {
        borderColor = "#22c55e";
        backgroundColor = "rgba(34,197,94,0.15)";
    }
    else if (status === "turun") {
        borderColor = "#ef4444";
        backgroundColor = "rgba(239,68,68,0.15)";
    }
    else {
        borderColor = "#2563eb";
        backgroundColor = "rgba(37,99,235,0.15)";
    }

    new Chart(canvas,{
        type:"line",
        data:{
            labels:tanggal,
            datasets:[{
                data:harga,
                borderColor: borderColor,
                backgroundColor:backgroundColor,
                fill:true,
                tension:.35,
                borderWidth:3,
                pointRadius:2
            }]
        },

        options:{
            responsive:true,
            maintainAspectRatio:false,
            animation:false,
            plugins:{
                legend:{
                    display:false
                },
                tooltip:{
                    callbacks:{
                        label:function(context){
                            return "Rp " +
                            context.parsed.y.toLocaleString("id-ID");

                        }
                    }
                }
            },

            scales:{
                x:{
                    display:false
                },
                y:{
                    display:false
                }
            }
        }
    });
});