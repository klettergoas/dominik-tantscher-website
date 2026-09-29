/** Leerzeichen durch geschützte ersetzen, damit z. B. Telefonnummern nicht umbrechen. */
export const nbsp = (text: string) => text.replace(/ /g, ' ');
