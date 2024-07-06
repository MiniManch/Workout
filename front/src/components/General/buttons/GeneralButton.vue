<template>
    <button class="button-80" @click="handleClick" role="button">{{ buttonText }}</button>
</template>
  
<script>
export default {
props: {
    buttonText: {
    type: String,
    required: true
    }
},
methods: {
    handleClick() {
    this.$emit('clicked');
    }
}
};
</script>

<style scoped>

.button-80 {
    background-color: rgba(130, 130, 130, 0.4);
    backface-visibility: hidden;
    border-radius: .375rem;
    border-style: solid;
    border-width: .125rem;
    border-color:transparent;
    box-sizing: border-box;
    color: white;
    cursor: pointer;
    display: inline-block;
    font-family: "Jost";
    letter-spacing: -.01em;
    line-height: 1.3;
    padding: .875rem 1.125rem;
    position: relative;
    text-align: left;
    text-decoration: none;
    transform: translateZ(0) scale(1);
    transition: transform .2s;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
}

.button-80:not(:disabled):hover {
    transform: scale(1.05); 
}

.button-80:not(:disabled):hover:active {
    transform: scale(1.05) translateY(.125rem);
}

.button-80:focus {
    outline: 0 solid transparent;
}

.button-80:focus:before {
    content: "";
    left: calc(-1*.375rem);
    pointer-events: none;
    position: absolute;
    top: calc(-1*.375rem);
    transition: border-radius;
    user-select: none;
}

.button-80:focus:not(:focus-visible) {
    outline: 0 solid transparent;
}

.button-80:focus:not(:focus-visible):before {
    border-width: 0;
}

.button-80:not(:disabled):active {
    transform: translateY(.125rem); 
}
</style>
