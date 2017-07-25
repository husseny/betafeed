var app = angular.module('homeApp', ['ngAnimate', 'ui.bootstrap']);

app.config(function($interpolateProvider, $httpProvider) {
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	$httpProvider.defaults.enctype="multipart/form-data";
});

app.factory('Scopes', function ($rootScope) {
	var mem = {};
 
	return {
		store: function (key, value) {
			$rootScope.$emit('scope.stored', key);
			mem[key] = value;
		},
		get: function (key) {
			return mem[key];
		}
	};
});

app.controller('homeCtrl', ['$scope', '$http', '$window', 'Scopes',  function userCtrl ($scope, $http, $window, Scopes){
	$scope.feed_index = 0;
	$scope.tweets = twitter_feed;
	$scope.open_status = function(status_id){
		$window.open('https://twitter.com/statuses/'+status_id);
	};
	$scope.open_profile = function(screen_name){
		$window.open('https://twitter.com/'+screen_name);
	}
}]);

app.animation('.slide-left-animation', function ($window) {
    return {
        enter: function (element, done) {
            TweenMax.fromTo(element, 1, { left: $window.innerWidth}, {left: 0, onComplete: done});
        },
        leave: function (element, done) {
        TweenMax.to(element, 1, {left: -$window.innerWidth, onComplete: done});
    }
};
});