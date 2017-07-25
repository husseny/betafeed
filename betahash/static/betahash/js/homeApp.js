var app = angular.module('homeApp', []);

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
	$scope.feed_index = 1;
	$scope.feed_title = "Twitter";
	$scope.tweets = twitter_feed;
	$scope.reddit_posts = reddit_feed;
	$scope.loading = false;
	
	$scope.open_url = function(url){
		$window.open(url);
	};

	$scope.toggle_feed = function(new_feed_index){
		$scope.toggled = false;
		if(new_feed_index != $scope.feed_index)
			$scope.toggled = true;
		switch(new_feed_index){
			case 1:
				$scope.feed_index = 1; $scope.feed_title = "Twitter";
			break;
			case 2:
				$scope.feed_index = 2; $scope.feed_title = "Reddit";
			break;
			case 3:
				$scope.feed_index = 3; $scope.feed_title = "Hackernews";
			break;
		}
		if($scope.toggled && ($scope.feed_index == 1 || $scope.feed_index == 2))
			$scope.refresh_feed();
	}

	$scope.refresh_feed = function(){
		if($scope.filter_query && $scope.filter_query.length > 0 && ! $scope.loading){
			$scope.loading = true;
			$post_data = { params:{feed_index: $scope.feed_index, filter_query: $scope.filter_query}};
			$http.get(site_url+'refresh_feed/', $post_data).success(function(data){
				console.log(data);
				if(data != -1){
					json_data = JSON.parse(data['feed']);
					if($scope.feed_index == 1)
						$scope.tweets = json_data;
					else
						$scope.reddit_posts = json_data;
				}
				$scope.loading = false;
				
			}).error(function(data){
				console.log("ERROR");
				$scope.loading = false;
			});
		}
	};

	$scope.reset_feed = function(){
		if(!$scope.filter_query && ! $scope.loading){
			$scope.loading = true;
			$post_data = {feed_index: $scope.feed_index};
			$http.get(site_url+'reset_feed/', $post_data).success(function(data){
				if(data != -1){
					json_data = JSON.parse(data['feed']);
					if($scope.feed_index == 1)
						$scope.tweets = json_data;
					else
						$scope.reddit_posts = json_data;
				}
				$scope.loading = false;
				
			}).error(function(data){
				console.log("ERROR");
				$scope.loading = false;
			});
		}
	};
}]);