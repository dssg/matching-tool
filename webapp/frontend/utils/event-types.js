import {filter, map, uniq} from 'ramda'

export function validEventTypes(jurisdictionRoles, currentJurisdiction) {
  const isCurrentJurisdiction = (role) => role.jurisdictionSlug === currentJurisdiction.slug
  const matchingRoles = filter(isCurrentJurisdiction, jurisdictionRoles)
  const extractProvider = (jurisdictionRole) => {
    return {
      slug: jurisdictionRole.eventTypeSlug,
      name: jurisdictionRole.eventType
    }
  }
  const rows = uniq(map(extractProvider, matchingRoles))
  return rows
}
