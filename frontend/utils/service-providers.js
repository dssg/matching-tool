import {filter, map, uniq} from 'ramda'

export function validServiceProviders(jurisdictionRoles, currentJurisdiction) {
  console.log('in valid service providers')
  console.log(jurisdictionRoles)
  console.log(currentJurisdiction)
  const isCurrentJurisdiction = (role) => role.jurisdictionSlug === currentJurisdiction.slug
  console.log(isCurrentJurisdiction)
  console.log(jurisdictionRoles)
  const matchingRoles = filter(isCurrentJurisdiction, jurisdictionRoles)
  const extractProvider = (jurisdictionRole) => {
    return {
      slug: jurisdictionRole.serviceProviderSlug,
      name: jurisdictionRole.serviceProvider
    }
  }
  const rows = uniq(map(extractProvider, matchingRoles))
  return rows
}
