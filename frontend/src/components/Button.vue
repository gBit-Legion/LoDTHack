<template>
  <button
    :class="
      $attrs.classes ||
      'bg-idealRed hover:shadow-innerMax text-white font-bold w-64 h-10'
    "
  >
    <p class="mr-2 mt-[2.5px]">
      {{ label }}
    </p>
  </button>
</template>
<script>
export default {
  props: {
    label: {
      type: String
    }
  }
}
</script>
