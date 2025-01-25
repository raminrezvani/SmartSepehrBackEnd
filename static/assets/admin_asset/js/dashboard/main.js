// ///////////////////////////////////////// SESSIONS
const visit_loading = () => {
    $("#visit_chart").html('<div class="spinner-border mt-3" role="status"></div>');
    $(".sessions .button-visit-chart").attr('disabled', 'disabled');
};

const visit_error = () => {
    const img_sec = '<img class="w-25 mx-auto text-center" alt="dashboard_error" src="/static/image/dashboard/Computer troubleshooting-pana.svg"/>'
    $("#visit_chart").html(img_sec);
};

const get_visits = (days) => {
    const url = `/admin/ga4-charts/?days=${days}&analyse_type=sessions`;

    const option_buttons = $(".sessions .button-visit-chart");
    const active_button = $(`.sessions .button-visit-chart[data-days='${days}']`);

    option_buttons.removeClass('btn-primary');
    option_buttons.addClass('btn-outline-primary');
    active_button.removeClass('btn-outline-primary');
    active_button.addClass('btn-primary');

    visit_loading();

    $.get(url).then(r => {
        if (r.status) {
            const options = {
                series: [{
                    name: "Session",
                    data: r.data.map(d => parseInt(d.views)),
                }],
                chart: {
                    height: 350,
                    type: 'line',
                    zoom: {
                        enabled: false
                    }
                },
                dataLabels: {
                    enabled: false
                },
                stroke: {
                    // curve: 'smooth'
                    curve: 'smooth'
                },
                title: {
                    show: false,
                    text: '',
                    align: 'left'
                },
                grid: {
                    row: {
                        colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                        opacity: 0.5
                    },
                },
                xaxis: {
                    categories: r.data.map(d => d.date),
                }
            };


            $("#visit_chart").html('')

            const chart = new ApexCharts(document.querySelector("#visit_chart"), options);
            chart.render();
        } else {
            visit_error();
        }
        option_buttons.removeAttr('disabled');
        active_button.attr('disabled', 'disabled');
    }).catch(e => {
        visit_error();
        option_buttons.removeAttr('disabled');
        active_button.attr('disabled', 'disabled');
    })
};

// ///////////////////////////////////////// TOTAL USERS
const total_users_loading = () => {
    $("#total_user_chart").html('<div class="spinner-border mt-3" role="status"></div>');
    $(".total_users .button-visit-chart").attr('disabled', 'disabled');
};

const total_users_error = () => {
    const img_sec = '<img class="w-25 mx-auto text-center" alt="dashboard_error" src="/static/image/dashboard/Computer troubleshooting-pana.svg"/>'
    $("#total_user_chart").html(img_sec);
};
const get_total_users = (days) => {
    const url = `/admin/ga4-charts/?days=${days}&analyse_type=activeUsers`;

    const option_buttons = $(".total_users .button-visit-chart");
    const active_button = $(`.total_users .button-visit-chart[data-days='${days}']`);

    option_buttons.removeClass('btn-primary');
    option_buttons.addClass('btn-outline-primary');
    active_button.removeClass('btn-outline-primary');
    active_button.addClass('btn-primary');

    total_users_loading();

    $.get(url).then(r => {
        if (r.status) {
            const options = {
                series: [{
                    name: "Active Users",
                    data: r.data.map(d => parseInt(d.views)),
                }],
                chart: {
                    height: 350,
                    type: 'line',
                    zoom: {
                        enabled: false
                    }
                },
                colors: ['#128f76'],
                dataLabels: {
                    enabled: false
                },
                stroke: {
                    // curve: 'smooth'
                    curve: 'smooth'
                },
                title: {
                    show: false,
                    text: '',
                    align: 'left'
                },
                grid: {
                    row: {
                        colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                        opacity: 0.5
                    },
                },
                xaxis: {
                    categories: r.data.map(d => d.date),
                }
            };


            $("#total_user_chart").html('')

            const chart = new ApexCharts(document.querySelector("#total_user_chart"), options);
            chart.render();
        } else {
            total_users_error();
        }
        option_buttons.removeAttr('disabled');
        active_button.attr('disabled', 'disabled');
    }).catch(e => {
        total_users_error();
        option_buttons.removeAttr('disabled');
        active_button.attr('disabled', 'disabled');
    })
};

// ///////////////////////////////////////// ENGAGEMENT RATE
const engagement_rate_loading = () => {
    $("#engagement_rate_chart").html('<div class="spinner-border mt-3" role="status"></div>');
    $(".engagement_rate .button-visit-chart").attr('disabled', 'disabled');
};

const engagement_rate_error = () => {
    const img_sec = '<img class="w-25 mx-auto text-center" alt="dashboard_error" src="/static/image/dashboard/Computer troubleshooting-pana.svg"/>'
    $("#engagement_rate_chart").html(img_sec);
};
const get_engagement_rate = (days) => {
    // const url = `/admin/ga4-charts/?days=${days}&analyse_type=engagementRate`;
    const url = `/admin/ga4-charts/?days=${days}&analyse_type=newUsers`;

    const option_buttons = $(".engagement_rate .button-visit-chart");
    const active_button = $(`.engagement_rate .button-visit-chart[data-days='${days}']`);

    option_buttons.removeClass('btn-primary');
    option_buttons.addClass('btn-outline-primary');
    active_button.removeClass('btn-outline-primary');
    active_button.addClass('btn-primary');

    engagement_rate_loading();

    $.get(url).then(r => {
        if (r.status) {
            const options = {
                series: [{
                    name: "New Users",
                    // data: r.data.map(d => Number(Number(d.views) * 100).toFixed(2)),
                    data: r.data.map(d => Number(d.views)),
                }],
                chart: {
                    height: 350,
                    type: 'line',
                    zoom: {
                        enabled: false
                    }
                },
                colors: ["#f39c12"],
                dataLabels: {
                    enabled: false
                },
                stroke: {
                    // curve: 'smooth'
                    curve: 'smooth'
                },
                title: {
                    show: false,
                    text: '',
                    align: 'left'
                },
                grid: {
                    row: {
                        colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                        opacity: 0.5
                    },
                },
                xaxis: {
                    categories: r.data.map(d => d.date),
                }
            };


            $("#engagement_rate_chart").html('')

            const chart = new ApexCharts(document.querySelector("#engagement_rate_chart"), options);
            chart.render();
        } else {
            engagement_rate_error();
        }
        option_buttons.removeAttr('disabled');
        active_button.attr('disabled', 'disabled');
    }).catch(e => {
        engagement_rate_error();
        option_buttons.removeAttr('disabled');
        active_button.attr('disabled', 'disabled');
    })
};


// ///////////////////////////////////////// DOCUMENT READY
$(document).ready(() => {
    get_visits(7);
    get_total_users(7);
    get_engagement_rate(7);
});