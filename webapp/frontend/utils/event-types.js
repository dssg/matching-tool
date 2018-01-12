import {filter, map, uniq} from 'ramda'

export function validEventTypes(jurisdictionRoles, currentJurisdiction) {
  console.log('in valid event types')
  console.log(jurisdictionRoles)
  console.log(currentJurisdiction)
  const isCurrentJurisdiction = (role) => role.jurisdictionSlug === currentJurisdiction.slug
  console.log(isCurrentJurisdiction)
  console.log(jurisdictionRoles)
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
