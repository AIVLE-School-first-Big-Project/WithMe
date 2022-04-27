'use strict';

var timerSetup = {
	template: '\n\t<form>\n\t\t <label for="min">Minutes<br />\n\t\t <input type="number" v-model="minutes" name="time_m" id="min" min="0" max="59">\n\t\t </label>\n\t\t <label for="sec">Secondes<br />\n\t\t\t  <input type="number" v-model="secondes" name="time_s" id="sec" max="59" min="0">\n\t\t </label>\n\t\t <button type="button" @click="sendTime">Set time</button>\n\t</form>',
	data: function data() {
		return {
			minutes: 0,
			secondes: 0
		};
	},

	methods: {
		sendTime: function sendTime() {
			this.$emit('set-time', { minutes: this.minutes, secondes: this.secondes });
		}
	}
};

var Timer = {
	template: '\n\t\t <div class="timer">{{ time | prettify }}</div>\n\t',
	props: ['time'],
	filters: {
		prettify: function prettify(value) {
			var data = value.split(':');
			var minutes = data[0];
			var secondes = data[1];
			if (minutes < 10) {
				minutes = "0" + minutes;
			}
			if (secondes < 10) {
				secondes = "0" + secondes;
			}
			return minutes + ":" + secondes;
		}
	}
};

var app = new Vue({
	el: "#app",
	components: {
		'timer-setup': timerSetup,
		'timer': Timer
	},
	data: {
		isRunning: false,
		minutes: 0,
		secondes: 0,
		time: 0,
		timer: null,
		sound: new Audio("http://s1download-universal-soundbank.com/wav/nudge.wav")
	},
	computed: {
		prettyTime: function prettyTime() {
			var time = this.time / 60;
			var minutes = parseInt(time);
			var secondes = Math.round((time - minutes) * 60);
			return minutes + ":" + secondes;
		}
	},
	methods: {
		start: function start() {
			var _this = this;

			this.isRunning = true;
			if (!this.timer) {
				this.timer = setInterval(function () {
					if (_this.time > 0) {
						_this.time--;
					} else {
						clearInterval(_this.timer);
						_this.sound.play();
						_this.reset();
					}
				}, 1000);
			}
		},
		stop: function stop() {
			this.isRunning = false;
			clearInterval(this.timer);
			this.timer = null;
		},
		reset: function reset() {
			this.stop();
			this.time = 0;
			this.secondes = 0;
			this.minutes = 0;
		},
		setTime: function setTime(payload) {
			this.time = payload.minutes * 60 + payload.secondes;
		}
	}
});
