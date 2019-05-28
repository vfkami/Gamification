/*
 * QRCodeReader.swift
 *
 * Copyright 2014-present Yannick Loriot.
 * http://yannickloriot.com
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 */

import AVFoundation
import UIKit

class ViewController: UIViewController, QRCodeReaderViewControllerDelegate {
    
    var part:String=""
    var sess:String=""
    
    @IBOutlet weak var dropDown: DropDown!{
        didSet{
            // The list of array to display. Can be changed dynamically
            dropDown.optionArray = ["Join", "Question", "Optout"]
            //Its Id Values and its optional
            //dropDown.optionIds = [1,23,54,22]
            // The the Closure returns Selected Index and String
            dropDown.didSelect{(selectedText , index ,id) in
                self.part=selectedText
                //self.valueLabel.text = "Selected String: \(selectedText) \n index: \(index)"
            }
        }
    }
    
    
    @IBOutlet weak var dropDownSess: DropDown!{
        didSet{
            // The list of array to display. Can be changed dynamically
            
            
            let originalString = "http://sbrc.inf.ufrgs.br/sessions"
            let escapedString = originalString.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed)!
            let url = URL(string:escapedString)
            
            let task = URLSession.shared.dataTask(with: url!) { (data,response,error) in
                if error == nil {
                    print("yay")
                    let responseData = String(data: data!, encoding: String.Encoding.utf8)
                    
                    let stringer=String(responseData!)
                    
                    let list = stringer.split(separator: ",").map(String.init)
                    
                    self.dropDownSess.optionArray = list
                }
                else
                {
                    print(error)
                }
            }
            task.resume()
            
            
//            dropDownSess.optionArray = ["ST-1","ST-2","ST-3","ST-4","ST-5","ST-6","ST-7","ST-8","ST-9","ST-10","ST-11","ST-12","ST-13","ST-14","ST-15","ST-16","ST-17","ST-18","ST-19","ST-20","ST-21","ST-22","ST-23","Hackathon","Courb","CTD-M","CTD-D","LANCOMM","WRNP","WCGA","WSCDC","WSlice","WBlockchain","WPEIF","WGRS","WTF","IIWTG","SF","Keynote Theo","Keynote Justine","Keynote Timothy","Keynote Walter","Tutorial Timothy","MC-1","MC-2","MC-3","MC-4","MC-5","MC-6"]
            //Its Id Values and its optional
            //dropDown.optionIds = [1,23,54,22]
            // The the Closure returns Selected Index and String
            dropDownSess.didSelect{(selectedText , index ,id) in
                self.sess=selectedText
                //self.valueLabel.text = "Selected String: \(selectedText) \n index: \(index)"
            }
        }
    }
    
    
    
  @IBOutlet weak var previewView: QRCodeReaderView! {
    didSet {
      previewView.setupComponents(with: QRCodeReaderViewControllerBuilder {
        $0.reader                 = reader
        $0.showTorchButton        = false
        $0.showSwitchCameraButton = false
        $0.showCancelButton       = false
        $0.showOverlayView        = true
        $0.rectOfInterest         = CGRect(x: 0.2, y: 0.2, width: 0.6, height: 0.6)
      })
    }
  }
  lazy var reader: QRCodeReader = QRCodeReader()
  lazy var readerVC: QRCodeReaderViewController = {
    let builder = QRCodeReaderViewControllerBuilder {
      $0.reader                  = QRCodeReader(metadataObjectTypes: [.qr], captureDevicePosition: .back)
      $0.showTorchButton         = true
      $0.preferredStatusBarStyle = .lightContent
      $0.showOverlayView        = true
      $0.rectOfInterest          = CGRect(x: 0.2, y: 0.2, width: 0.6, height: 0.6)
      
      $0.reader.stopScanningWhenCodeIsFound = false
    }
    
    return QRCodeReaderViewController(builder: builder)
  }()

  // MARK: - Actions

  private func checkScanPermissions() -> Bool {
    do {
        if self.part == "" || self.sess == "" {throw NSError(domain: "com.yannickloriot.error", code: -322, userInfo: nil)}
      return try QRCodeReader.supportsMetadataObjectTypes()
    } catch let error as NSError {
      let alert: UIAlertController

      switch error.code {
      case -322:
        alert = UIAlertController(title: "Error", message: "Don't Leave Fields Blank My Friend :-)", preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .cancel, handler: nil))
      case -11852:
        alert = UIAlertController(title: "Error", message: "This app is not authorized to use Back Camera.", preferredStyle: .alert)

        alert.addAction(UIAlertAction(title: "Setting", style: .default, handler: { (_) in
          DispatchQueue.main.async {
            if let settingsURL = URL(string: UIApplication.openSettingsURLString) {
              UIApplication.shared.openURL(settingsURL)
            }
          }
        }))

        alert.addAction(UIAlertAction(title: "Cancel", style: .cancel, handler: nil))
      default:
        alert = UIAlertController(title: "Error", message: "Reader not supported by the current device", preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .cancel, handler: nil))
      }

      present(alert, animated: true, completion: nil)

      return false
    }
  }

  @IBAction func scanInModalAction(_ sender: AnyObject) {
    guard checkScanPermissions() else { return }
    
    readerVC.modalPresentationStyle = .formSheet
    readerVC.delegate               = self

    readerVC.completionBlock = { (result: QRCodeReaderResult?) in
      if let result = result {
        print("Completion with result: \(result.value) of type \(result.metadataType)")
        let originalString = "https://sbrc.d4c.wtf/qr/"+result.value+"/"+self.sess+"/"+self.part
        let escapedString = originalString.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed)!
        let url = URL(string:escapedString)
      
        let task = URLSession.shared.dataTask(with: url!) { (data,response,error) in
            if error == nil {
                print("yay")
            }
            else
            {
                print(error)
            }
        }
        task.resume()
        
        }
    }

    present(readerVC, animated: true, completion: nil)
  }

  @IBAction func scanInPreviewAction(_ sender: Any) {
    guard checkScanPermissions(), !reader.isRunning else { return }

    reader.didFindCode = { result in
      print("Completion with result: \(result.value) of type \(result.metadataType)")
        
    }

    reader.startScanning()
  }

  // MARK: - QRCodeReader Delegate Methods

  func reader(_ reader: QRCodeReaderViewController, didScanResult result: QRCodeReaderResult) {
    reader.stopScanning()

    dismiss(animated: true) { [weak self] in
      let alert = UIAlertController(
        title: "QRCodeReader",
        message: String (format:"%@ (of type %@)", result.value, result.metadataType),
        preferredStyle: .alert
      )
      alert.addAction(UIAlertAction(title: "OK", style: .cancel, handler: nil))

      self?.present(alert, animated: true, completion: nil)
    }
  }

  func reader(_ reader: QRCodeReaderViewController, didSwitchCamera newCaptureDevice: AVCaptureDeviceInput) {
    print("Switching capture to: \(newCaptureDevice.device.localizedName)")
  }

  func readerDidCancel(_ reader: QRCodeReaderViewController) {
    reader.stopScanning()

    dismiss(animated: true, completion: nil)
  }
}
