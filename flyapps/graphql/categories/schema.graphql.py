type Category {
    id: ID!,
    name: String!,
    slug: String,
    description: String,
    threads: [Thread]
}

input CategoryCreateInput {
    id: ID,
    name: String,
    description: String,
    slug: String,
}

input CategoryEditPatchInput {
    name: String,
    description: String,
    slug: String,
}

input CategoryEditInput {
    id: Int,
    slug: String,
    patch: CategoryEditPatchInput
}

input CategoryDeleteInput {
    id: Int,
    slug: String
}

type CategoryCreatePayload {
    category: Category
}

type CategoryDeletePayload {
    category: [Category]
}

type CategoryEditPayload {
    category: Category
}

type Mutation {
    categoryCreate (input: CategoryCreateInput): CategoryCreatePayload,
    categoryDelete (input: CategoryDeleteInput): CategoryDeletePayload,
    categoryEdit (input: CategoryEditInput): CategoryEditPayload,
}

type Query {
    getAllCategories() categories: [Category],
    getCategoryByIdAndSlug(id: ID!, slug: String!) category(id, slug): [Thread]
}

schema {
    query: Query,
    mutation: Mutation,
}