from gql import gql

query_get_repos = gql("""query getRepositories(
    $organization: String!
    $take: Int
    $after: String){
    organization(login: $organization) {
        repositories(first: $take, after: $after) {
            nodes {
                id
                name
                url
                createdAt
                databaseId
                description
                defaultBranchRef {
                    name
                    target {
                        commitUrl
                        ... on Commit {
                            commitUrl
                            committedDate
                        }
                    }
                }
                languages(first: 100) {
                    edges {
                        size
                        node {
                            name
                            id
                        }
                    }
                }
            }
            pageInfo {
                endCursor
                hasNextPage
            }
        }
    }
}""")