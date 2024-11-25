// pages/api/funcoesDeConcilia.js
import * as conciliaApsenDimed from '../scripts/conciliacao_apsen_dimed.py';
import * as conciliaApsenGam from '../scripts/conciliacao_apsen_gam.py';
import * as conciliaApsenGjb from '../scripts/conciliacao_apsen_gjb.py';
import * as conciliaApsenGsc from '../scripts/conciliacao_apsen_gsc.py';
import * as conciliaMsdAgille from '../scripts/conciliacao_msd_agille.py';
import * as conciliaMsdGsc from '../scripts/conciliacao_msd_gsc.py';
import * as conciliaOrganonGsc from '../scripts/conciliacao_organon_gsc.py';
import * as conciliaBayerGsc from '../scripts/conciliacao_bayer_gsc.py';

export async function processarConciliação(baseFuncional, baseDistribuidor, pfMargem, industria, distribuidor) {
  try {
    let resultado;

    // Escolhe a lógica de conciliação com base na indústria e distribuidor
    if (industria === 'apsen') {
      switch (distribuidor) {
        case 'dimed':
          resultado = await conciliaApsenDimed.processar(baseFuncional, baseDistribuidor, pfMargem, industria);
          break;
        case 'gam':
          resultado = await conciliaApsenGam.processar(baseFuncional, baseDistribuidor, pfMargem, industria);
          break;
        case 'gjb':
          resultado = await conciliaApsenGjb.processar(baseFuncional, baseDistribuidor, pfMargem, industria);
          break;
        case 'gsc':
          resultado = await conciliaApsenGsc.processar(baseFuncional, baseDistribuidor, pfMargem, industria);
          break;
        default:
          throw new Error(`Distribuidor ${distribuidor} não encontrado para a indústria APSEN.`);
      }
    } else if (industria === 'msd') {
      switch (distribuidor) {
        case 'agille':
          resultado = await conciliaMsdAgille.processar(baseFuncional, baseDistribuidor, pfMargem, industria);
          break;
        case 'gsc':
          resultado = await conciliaMsdGsc.processar(baseFuncional, baseDistribuidor, pfMargem, industria);
          break;
        default:
          throw new Error(`Distribuidor ${distribuidor} não encontrado para a indústria MSD.`);
      }
    } else if (industria === 'organon') {
      if (distribuidor === 'gsc') {
        resultado = await conciliaOrganonGsc.processar(baseFuncional, baseDistribuidor, pfMargem, industria);
      } else {
        throw new Error(`Distribuidor ${distribuidor} não encontrado para a indústria ORGANON.`);
      }
    } else if (industria === 'bayer') {
      if (distribuidor === 'gsc') {
        resultado = await conciliaBayerGsc.processar(baseFuncional, baseDistribuidor, pfMargem, industria);
      } else {
        throw new Error(`Distribuidor ${distribuidor} não encontrado para a indústria BAYER.`);
      }
    } else {
      throw new Error(`Indústria ${industria} não encontrada.`);
    }

    // Retorna o buffer com o resultado da conciliação para download
    return resultado;

  } catch (error) {
    console.error("Erro ao processar conciliação:", error);
    throw new Error("Falha ao processar a conciliação");
  }
}
