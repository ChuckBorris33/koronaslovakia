<script lang="ts">
  import { Pagination, PaginationItem, PaginationLink } from "sveltestrap";

  export let limit: number;
  export let offset: number;
  export let length: number;

  let pageCount: number;
  let actualPage: number;
  let pages: number[] = [];

  function setOffset(event: Event, page: number) {
    event.preventDefault();
    offset = (page - 1) * limit;
  }

  $: {
    pages = [];
    pageCount = Math.ceil(length / (limit * 1.0));
    actualPage = Math.ceil(offset / (limit * 1.0)) + 1;

    for (let i = 1; i <= pageCount; i++) {
      pages.push(i);
    }
  }
</script>

<div class="d-flex w-100 justify-content-end">
  <Pagination>
    <PaginationItem disabled={actualPage == 1}>
      <PaginationLink first on:click={(event) => setOffset(event, 1)} />
    </PaginationItem>
    <PaginationItem disabled={actualPage == 1}>
      <PaginationLink
        previous
        on:click={(event) => setOffset(event, actualPage - 1)} />
    </PaginationItem>
    {#each pages as page}
      <PaginationItem active={page == actualPage}>
        <PaginationLink on:click={(event) => setOffset(event, page)}>
          {page}
        </PaginationLink>
      </PaginationItem>
    {/each}
    <PaginationItem disabled={actualPage == pageCount}>
      <PaginationLink
        next
        on:click={(event) => setOffset(event, actualPage + 1)} />
    </PaginationItem>
    <PaginationItem disabled={actualPage == pageCount}>
      <PaginationLink last on:click={(event) => setOffset(event, pageCount)} />
    </PaginationItem>
  </Pagination>
</div>
