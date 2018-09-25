<template>
<section class="container">
    <h1>Taggle</h1>
    <p>Find Kaggle competitions with various tags.</p>
    <span v-if="loading">now loading...</span>
    <table class="table table-hover" v-if="!loading">
        <thead>
            <tr>
                <th scope="col"></th>
                <th scope="col">Name</th>
                <th scope="col">Tags</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="compe in competitions" :key="compe.id">
                <th scope="row"><img :src="compe.image" alt="" width=32 height=32></th>
                <td><a :href="compe.url">{{compe.name}}</a></td>
                <td></td>
            </tr>
        </tbody>
    </table>
</section>
</template>

<script>
import db from './firebaseInit'
export default {
  name: 'home',
  data () {
    return {
      competitions: [],
      loading: true
    }
  },
  created () {
    db.collection('competitions').get().then((snapshot) => {
      this.loading = false
      snapshot.forEach((doc) => {
        let data = {
          'id': doc.id,
          'name': doc.data().name,
          'url': 'http://www.kaggle.com' + doc.data().url,
          'image': doc.data().image
        }
        this.competitions.push(data)
      })
    })
  }
}
</script>
