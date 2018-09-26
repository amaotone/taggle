<template>
<section class="container">
  <div class="jumbotron">
    <h1 class="display-5">Taggle</h1>
    <p class="lead">Find Kaggle competitions with various tags.</p>
    <input type="text" class="form-control" placeholder="search">
  </div>
  <span v-if="loading">now loading...</span>
  <table class="table" v-if="!loading">
    <thead>
      <tr>
        <th scope="col"></th>
        <th scope="col">Name</th>
        <th scope="col">Tags</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="compe in competitions.sort((a, b) => b.startdate-a.startdate)" :key="compe.id">
        <th class="align-middle" scope="row"><img class="rounded" :src="compe.image" alt="" width=60 height=60></th>
        <td class="align-middle">
          <a :href="compe.url">{{compe.name}}</a>
          <br>
          from {{compe.startdate.format('YYYY-MM-DD')}} to {{compe.enddate.format('YYYY-MM-DD')}}
        </td>
        <td class="align-middle"><span v-for="tag in Object.keys(compe.tags)" :key="tag" class="badge badge-dark m-1">{{tag}}</span></td>
      </tr>
    </tbody>
  </table>
</section>
</template>

<script>
import db from './firebaseInit'
var moment = require('moment')
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
          'startdate': moment(doc.data().start),
          'enddate': moment(doc.data().end),
          'image': doc.data().image,
          'tags': doc.data().tags
        }
        this.competitions.push(data)
      })
    })
  }
}
</script>
<style>
body {
  font-size: 14px;
}
</style>
