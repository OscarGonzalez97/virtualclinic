(function($) {
    "use strict";
        
    // Navbar Menu JS
    $(window).on('scroll', function() {
        if ($(this).scrollTop() > 80) {
            $('.top-menu').addClass('menu-shrink');
        } else {
            $('.top-menu').removeClass('menu-shrink');
        }
    });
    $('.navbar .navbar-nav li a').on('click', function(e) {
        var anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $(anchor.attr('href')).offset().top - 50
        }, 1000);
        e.preventDefault();
    });
    $(document).on('click','.navbar-collapse.show',function(e) {
        if( $(e.target).is('a') && $(e.target).attr('class') != 'dropdown-toggle' ) {
            $(this).collapse('hide');
        }
    });

    // Click smooth scroll
    $('.slide-button a').on('click', function(e) {
        var anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $(anchor.attr('href')).offset().top - 50
        }, 1000);
        e.preventDefault();
    });
    // End Click smooth scroll 

    // Homepage Slides JS
    $(".homepage-slides").owlCarousel({
        items: 1,
        nav: true,
        dots: false,
        touchDrag: false,
        mouseDrag: false,
        autoplay: false,
        //animateOut: 'fadeOut',
        autoplayHoverPause: true,
        loop: true,
        navText: ["<i class='icofont-long-arrow-left'></i>", "<i class='icofont-long-arrow-right'></i>"],
    });
    $(".homepage-slides").on("translate.owl.carousel", function() {
        $(".single-slider-item h1, .single-slider-item p").removeClass("animated animate__animated animate__fadeInUp").css("opacity", "0");
        $(".single-slider-item .slide-button a").removeClass("animated fadeInDown").css("opacity", "0");
    });
    $(".homepage-slides").on("translated.owl.carousel", function() {
        $(".single-slider-item h1, .single-slider-item p").addClass("animated animate__animated animate__fadeInUp").css("opacity", "1");
        $(".single-slider-item .slide-button a").addClass("animated fadeInDown").css("opacity", "1");
    });
    // End Homepage Slides JS

    // Popup Video JS
    $('.popup-youtube, .popup-vimeo').magnificPopup({
        disableOn: 300,
        type: 'iframe',
        mainClass: 'mfp-fade',
        removalDelay: 160,
        preloader: false,
        fixedContentPos: false,
    });
    // End Popup Video JS

    // WOW JS
    new WOW().init();

    // Screenshot Carousel JS
    $(".screenshot-carousel").owlCarousel({
        nav: true,
        margin: 30,
        dots: true,
        autoplay: true,
        autoplayHoverPause: true,
        smartSpeed: 500,
        loop: true,
        navText: ["<i class='icofont-swoosh-left'></i>", "<i class='icofont-swoosh-right'></i>"],
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 2
            },
            768: {
                items: 3
            },
            1200: {
                items: 4
            }
        }
    });
    // End Screenshot Carousel JS

    // Testimonial Carousel JS
    $(".testimonial-carousel").owlCarousel({
        items: 1,
        nav: false,
        dots: true,
        autoplay: false,
        margin: 40,
        smartSpeed: 500,
        autoplayHoverPause: true,
        loop: true,
        responsive: {
            0: {
                items: 1
            },
            758: {
                items: 2
            },
            1200: {
                items: 3
            }
        }
    });
    // End Testimonial Carousel JS

    // Particleground JS
    $('#particles').particleground({
        dotColor: '#5cbdaa',
        lineColor: '#5cbdaa'
    });
    $('.intro').css({
        'margin-top': -($('.intro').height() / 2)
    });
    // End Particleground JS

    // Faq Js
    $(".faq-panel > .faq-title").on("click", function() {
        if ($(this).hasClass('active')) {
            $(this).removeClass("active");
            $(this).siblings('.faq-textarea').slideUp(200);
            $(".faq-panel > .faq-title i").removeClass("icofont-minus").addClass("icofont-plus");
        } else {
            $(".faq-panel > .faq-title i").removeClass("icofont-minus").addClass("icofont-plus");
            $(this).find("i").removeClass("icofont-plus").addClass("icofont-minus");
            $(".faq-panel > .faq-title").removeClass("active");
            $(this).addClass("active");
            $('.faq-textarea').slideUp(200);
            $(this).siblings('.faq-textarea').slideDown(200);
        }
    });
    var accordion = (function() {
        var $accordion = $('.js-accordion');
        var $accordion_header = $accordion.find('.js-accordion-header');
        var $accordion_item = $('.js-accordion-item');
        var settings = {
            speed: 400,
            oneOpen: false
        };
        return {
            init: function($settings) {
                $accordion_header.on('click', function() {
                    accordion.toggle($(this));
                });
                $.extend(settings, $settings);
                if (settings.oneOpen && $('.js-accordion-item.active').length > 1) {
                    $('.js-accordion-item.active:not(:first)').removeClass('active');
                }
                $('.js-accordion-item.active').find('> .js-accordion-body').show();
            },
            toggle: function($this) {
                if (settings.oneOpen && $this[0] != $this.closest('.js-accordion').find('> .js-accordion-item.active > .js-accordion-header')[0]) {
                    $this.closest('.js-accordion').find('> .js-accordion-item').removeClass('active').find('.js-accordion-body').slideUp()
                }
                $this.closest('.js-accordion-item').toggleClass('active');
                $this.next().stop().slideToggle(settings.speed);
            }
        }
    })();
    $(document).ready(function() {
        accordion.init({
            speed: 300,
            oneOpen: true
        });
    });
    // End Faq Js

    // Back Top JS
    $('body').append('<div id="toTop" class="back-top-button"><i class="icofont-rocket"></i></div>');
    $(window).scroll(function() {
        if ($(this).scrollTop() != 0) {
            $('#toTop').fadeIn();
        } else {
            $('#toTop').fadeOut();
        }
    });
    $('#toTop').on('click', function() {
        $("html, body").animate({
            scrollTop: 0
        }, 600);
        return false;
    });
    // End Back Top JS

    // Subscribe form
    $(".newsletter-form").validator().on("submit", function (event) {
        if (event.isDefaultPrevented()) {
        // handle the invalid form...
            formErrorSub();
            submitMSGSub(false, "Please enter your email correctly.");
        } else {
            // everything looks good!
            event.preventDefault();
        }
    });
    function callbackFunction (resp) {
        if (resp.result === "success") {
            formSuccessSub();
        }
        else {
            formErrorSub();
        }
    }
    function formSuccessSub(){
        $(".newsletter-form")[0].reset();
        submitMSGSub(true, "Thank you for subscribing!");
        setTimeout(function() {
            $("#validator-newsletter").addClass('hide');
        }, 4000)
    }
    function formErrorSub(){
        $(".newsletter-form").addClass("animated shake");
        setTimeout(function() {
            $(".newsletter-form").removeClass("animated shake");
        }, 1000)
    }
    function submitMSGSub(valid, msg){
        if(valid){
            var msgClasses = "validation-success";
        } else {
            var msgClasses = "validation-danger";
        }
        $("#validator-newsletter").removeClass().addClass(msgClasses).text(msg);
    }
    // AJAX MailChimp
    $(".newsletter-form").ajaxChimp({
        url: "https://envytheme.us20.list-manage.com/subscribe/post?u=60e1ffe2e8a68ce1204cd39a5&amp;id=42d6d188d9", // Your url MailChimp
        callback: callbackFunction
    });
    jQuery(window).on('load', function() {
        jQuery(".preloader-wrap").fadeOut(500);
    });

    // CAR LANDING PAGE START

    // Homepage Slides JS
    $(".hero-slider-section").owlCarousel({
        items: 1,
        nav: false,
        dots: true,
        touchDrag: false,
        mouseDrag: false,
        autoplay: false,
        //animateOut: 'fadeOut',
        autoplayHoverPause: true,
        loop: true,
        navText: ["<i class='icofont-long-arrow-left'></i>", "<i class='icofont-long-arrow-right'></i>"],

    });
    //end home page two slider

    //project  slider
    $(".project-wrapper").owlCarousel({
        items: 4,
        nav: false,
        margin: 30,
        dots: true,
        autoplay: true,
        autoplayHoverPause: true,
        smartSpeed: 2000,
        loop: true,
        responsive: {
            0: {
                items: 1
            },
            575: {
                items: 2
            },
            758: {
                items: 2
            },
            1200: {
                items: 4
            }
        }
    });
    //end project slider

    // Navbar Menu JS
    $(window).on('scroll', function() {
        if ($(this).scrollTop() > 80) {
            $('.main-menu').addClass('menu-shrink');
        } else {
            $('.main-menu').removeClass('menu-shrink');
        }
    });
    // Navbar Menu JS end

    // Testimonial Carousel JS
    $(".feedback-wrapper").owlCarousel({
        items: 1,
        nav: false,
        dots: true,
        autoplay: true,
        margin: 40,
        smartSpeed: 500,
        autoplayHoverPause: true,
        loop: true,
        responsive: {
            0: {
                items: 1
            },
            575: {
                items: 2
            },
            758: {
                items: 2
            },
            1200: {
                items: 3
            }
        }
    });
    // Testimonial Carousel JS end
     
    // CAR LANDING PAGE END


    // SAAS LANDING PAGE START

    // Navbar Menu JS  
    $(window).on('scroll', function() {
        if ($(this).scrollTop() > 80) {
            $('.menu-3').addClass('menu-shrink');
        } else {
            $('.menu-3').removeClass('menu-shrink');
        }
    });
    // Navbar Menu JS end

    // Brand JS
    $(".brand-wrapper").owlCarousel({
        items: 5,
        nav: false,
        dots: true,
        autoplay: true,
        margin: 40,
        smartSpeed: 500,
        autoplayHoverPause: true,
        loop: true,
        responsive: {
            0: {
                items: 1
            },
            575: {
                items: 4
            },
            758: {
                items: 5
            },
            1200: {
                items: 5
            }
        }
    });
    // Brand JS

    // feedback JS
    $(".feedbacks-3").owlCarousel({
        items: 1,
        nav: false,
        dots: true,
        autoplay: true,
        margin: 40,
        smartSpeed: 500,
        autoplayHoverPause: true,
        loop: true,
    });
    // feedback JS

    // SAAS LANDING PAGE START

    // IT SOLUTION PAGE START

    // Brand JS
    $(".brand-wrapper-4").owlCarousel({
        items: 6,
        nav: false,
        dots: true,
        autoplay: true,
        margin: 40,
        smartSpeed: 500,
        autoplayHoverPause: true,
        loop: true,
        responsive: {
            0: {
                items: 1
            },
            575: {
                items: 4
            },
            758: {
                items: 5
            },
            1200: {
                items: 6
            }
        }
    });
    // Brand JS

    
    // Mixitup JS
    try {
        var mixer = mixitup('#Container', {
            controls: {
                toggleDefault: 'none'
            }
        });
    } catch (err) {}
    // Counter up Carousel JS end

    // Testimonial Carousel JS
    $('.slider-single').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: true,
        fade: false,
        adaptiveHeight: true,
        infinite: false,
        useTransform: true,
        speed: 1000,
        autoplay: true,
        cssEase: 'cubic-bezier(0.77, 0, 0.18, 1)',
    });
    $('.slider-nav')
        .on('init', function(event, slick) {
            $('.slider-nav .slick-slide.slick-current').addClass('is-active');
        })
        .slick({
            slidesToShow: 7,
            slidesToScroll: 7,
            dots: false,  
            focusOnSelect: false,
            infinite: false,
            responsive: [{
                breakpoint: 1024,
                settings: {
                    slidesToShow: 5,
                    slidesToScroll: 5,
                }
            }, {
                breakpoint: 640,
                settings: {
                    slidesToShow: 4,
                    slidesToScroll: 4,
               }
            }, {
                breakpoint: 420,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 3,
                }
            }]
        });
    $('.slider-single').on('afterChange', function(event, slick, currentSlide) {
        $('.slider-nav').slick('slickGoTo', currentSlide);
        var currrentNavSlideElem = '.slider-nav .slick-slide[data-slick-index="' + currentSlide + '"]';
        $('.slider-nav .slick-slide.is-active').removeClass('is-active');
        $(currrentNavSlideElem).addClass('is-active');
    });
    $('.slider-nav').on('click', '.slick-slide', function(event) {
        event.preventDefault();
        var goToSingleSlide = $(this).data('slick-index');
        $('.slider-single').slick('slickGoTo', goToSingleSlide);
    });
    // Testimonial Carousel JS end

    // Navbar Menu JS  
    $(window).on('scroll', function() {
        if ($(this).scrollTop() > 80) {
            $('.menu-4').addClass('menu-shrink');
        } else {
            $('.menu-4').removeClass('menu-shrink');
        }
    });
    // Navbar Menu JS end

    // IT SOLUTION PAGE END

    // REAL ESTATE PAGE START

    // Brand JS
    $(".project-wrappers").owlCarousel({
        nav: true,
        dots: false,
        autoplay: true,
        margin: 30,
        smartSpeed: 2000,
        autoplayHoverPause: true,
        loop: true,
        navText: ["<i class='flaticon-left-arrow'></i>", "<i class='flaticon-right-arrow'></i>"],
        responsive: {
            0: {
                items: 1
            },
            575: {
                items: 2
            },
            758: {
                items: 2
            },
            992: {
                items: 3
            },
            1200: {
                items: 4
            }
        }
    });
    // Brand JS

    //magnificPopup
    $('.popup-gallery').magnificPopup({
        delegate: 'a',
        type: 'image',
        tLoading: 'Loading image #%curr%...',
        mainClass: 'mfp-img-mobile',
        gallery: {
            enabled: true,
            navigateByImgClick: true,
            preload: [0,1]
        },
        image: {
            tError: '<a href="%url%">The image #%curr%</a> could not be loaded.',
            titleSrc: function(item) {
                return item.el.attr('title') + '<small>by Marsel Van Oosten</small>';
            },
        },
    });

    //tabs
    $("#user-nav-tabs li").on('click', function(e) {
        var targetLink = $(e.currentTarget.children[0]).attr("href").slice(1);
        var content_map = {
            c1  : "#content1",
            c2  : "#content2",
            c3  : "#content3"
        }
        $(e.currentTarget).siblings().removeClass("active");
        $.each(content_map, function(hash, elid) {
            if (hash == targetLink) {
                $(elid).show();
                $(e.currentTarget).addClass("active");
            } else {
                $(elid).hide();
            }
        });
    });
    // REAL ESTATE PAGE END

    // CHARITY LANDING PAGE START
    // Homepage Slides JS
    $(".charity-slides").owlCarousel({
        items: 1,
        nav: false,
        dots: true,
        touchDrag: false,
        mouseDrag: false,
        autoplay: false,
        //animateOut: 'fadeOut',
        autoplayHoverPause: true,
        loop: true,
        navText: ["<i class='icofont-long-arrow-left'></i>", "<i class='icofont-long-arrow-right'></i>"],
    });
    $(".charity-slides").on("translate.owl.carousel", function() {
        $(".single-slider-items h1, .single-slider-items p").removeClass("animated animate__animated animate__fadeInUp").css("opacity", "0");
        $(".single-slider-items .row").removeClass("animated fadeInDown").css("opacity", "0");
    });
    $(".charity-slides").on("translated.owl.carousel", function() {
        $(".single-slider-items h1, .single-slider-items p").addClass("animated animate__animated animate__fadeInUp").css("opacity", "1");
        $(".single-slider-items .row").addClass("animated fadeInDown").css("opacity", "1");
    });
    // End Homepage Slides JS

    //tabs
    $(document).ready(function() {
        $('#tabs li a').click(function(e) {
            $('#tabs li, #content .current').removeClass('current').removeClass('animate__animated animate__fadeInUp');
            $(this).parent().addClass('current');
            var currentTab = $(this).attr('href');
            $(currentTab).addClass('current animate__animated animate__fadeInUp');
            e.preventDefault();
        
        });
    });

    // Brand JS
    $(".causes-wrappers").owlCarousel({
        nav: false,
        dots: true,
        autoplay: true,
        margin: 30,
        smartSpeed: 2000,
        autoplayHoverPause: true,
        loop: true,
        responsive: {
            0: {
                items: 1
            },
            575: {
                items: 2
            },
            758: {
                items: 2
            },
            992: {
                items: 3
            },
            1200: {
                items: 4
            }
        }
    });
    // Brand JS

    // Testimonial Carousel JS
    $(".chrity-feedback-wrapper").owlCarousel({
        nav: false,
        dots: true,
        autoplay: true,
        margin: 20,
        smartSpeed: 500,
        autoplayHoverPause: true,
        loop: true,
        responsive: {
            0: {
                items: 1
            },
            575: {
                items: 2
            },
            758: {
                items: 2
            },
            1200: {
                items: 3
            }
        }
    });
    // Testimonial Carousel JS end

    // CHARITY LANDING PAGE END

    // Datepiker
    $( "#datepicker, #datepicker1" ).datepicker();

}(jQuery));

// function to set a given theme/color-scheme
function setTheme(themeName) {
	localStorage.setItem('heroapp_theme', themeName);
	document.documentElement.className = themeName;
}
// function to toggle between light and dark theme
function toggleTheme() {
	if (localStorage.getItem('heroapp_theme') === 'theme-dark') {
		setTheme('theme-light');
	} else {
		setTheme('theme-dark');
	}
}
// Immediately invoked function to set the theme on initial load
//(function () {
//	if (localStorage.getItem('heroapp_theme') === 'theme-dark') {
//		setTheme('theme-dark');
//		document.getElementById('slider').checked = false;
//	} else {
//		setTheme('theme-light');
//	document.getElementById('slider').checked = true;
//	}
//})();