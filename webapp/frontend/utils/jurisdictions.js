import {map, uniq} from 'ramda'

export function validJurisdictions(jurisdictionRoles) {
  const extractJurisdiction = (jurisdictionRole) => {
    return {
      slug: jurisdictionRole.jurisdictionSlug,
      name: jurisdictionRole.jurisdiction
    }
  }
  const rows = uniq(map(extractJurisdiction, jurisdictionRoles))
  return rows
}
